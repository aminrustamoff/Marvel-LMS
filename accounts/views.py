from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.utils.decorators import method_decorator
from .decorators import teacher_required
from .forms import UserCreateForm, UserUpdateForm, AdminPasswordResetForm, UserDeleteConfirmForm

from django.views.generic.edit import CreateView, UpdateView

from accounts.models import User


class RoleBasedLoginView(LoginView):
    template_name = "accounts/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == "STUDENT":
                return redirect("dashboard:student_dashboard")
            else:
                return redirect("dashboard:teacher_dashboard")

        return super().get(request, *args, **kwargs)
                

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        if self.request.user.role == User.Role.TEACHER:
            return reverse("dashboard:teacher_dashboard")
        return reverse("dashboard:student_dashboard")

@teacher_required
def student_list(request):
    students = User.objects.filter(role=User.Role.STUDENT)
    return render(request, "accounts/student_list.html", {"students": students})


@teacher_required
def student_detail(request, pk):
    student = User.objects.get(pk=pk, role=User.Role.STUDENT)
    return render(request, "accounts/student_detail.html", {"student": student})


@teacher_required
def teacher_list(request):
    teachers = User.objects.filter(role=User.Role.TEACHER)
    return render(request, "accounts/teacher_list.html", {"teachers": teachers})


@teacher_required
def teacher_detail(request, pk):
    teacher = User.objects.get(pk=pk, role=User.Role.TEACHER)
    return render(request, "accounts/teacher_detail.html", {"teacher": teacher})


@method_decorator(teacher_required, name="dispatch")
class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'accounts/user_form.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Teacher-Student bog'lanishini saqlash (agar shunday model bo'lsa)
        # self.object.teacher = self.request.user
        # self.object.save()

        generated = getattr(form, 'generated_password', None)
        if generated:
            messages.success(
                self.request,
                f"A user created. Login: {self.object.username}, Password: {generated}"
            )
        else:
            messages.success(self.request, "A user created successfully!")

        return response

    def get_success_url(self):
        if self.object.role == "STUDENT":
            return reverse('accounts:student_detail', kwargs={'pk': self.object.pk})
        if self.object.role == "TEACHER":
            return reverse('accounts:teacher_detail', kwargs={'pk': self.object.pk})
    

@method_decorator(teacher_required, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    def get_success_url(self):
            if self.object.role == "STUDENT":
                return reverse('accounts:student_detail', kwargs={'pk': self.object.pk})
            if self.object.role == "TEACHER":
                return reverse('accounts:teacher_detail', kwargs={'pk': self.object.pk})


@teacher_required
def password_reset(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Optional, but important for security: only allow teacher to reset password for students in their own groups
    # if user.teacher != request.user:
    #     return redirect('dashboard')

    if request.method == 'POST':
        form = AdminPasswordResetForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            messages.success(request, f"{user.username}'s password is renewed!")

            if user.role == "STUDENT":
                return redirect('accounts:student_detail', pk=user.pk)
            else:
                return redirect('accounts:teacher_detail', pk=user.pk)

    else:
        form = AdminPasswordResetForm()

    return render(request, 'accounts/password_reset_form.html', {
        'form': form,
        'target_user': user,
    })

@method_decorator(teacher_required, name="dispatch")
class UserDeleteView(LoginRequiredMixin, SingleObjectMixin, FormMixin, TemplateResponseMixin, View):
    model = User
    form_class = UserDeleteConfirmForm
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('dashboard:teacher_dashboard')
    context_object_name = 'object'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        deleted_username = self.object.username
        self.object.delete()
        messages.success(self.request, f"User '{deleted_username}' has been deleted.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))