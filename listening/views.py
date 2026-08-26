from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from accounts.decorators import teacher_required, student_required, TeacherRequiredMixin

from utils import text_to_html

from . import models
from .models import Listening
from assignments.models import ListeningTask
from progress.models import StudentProgress, ProgressListening

from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from .forms import ListeningForm, ListeningImageFormSet, DeleteConfirmForm

@teacher_required
def listening_list(request):
    listening = models.Listening.objects.all().order_by('-created_at')
    paginator = Paginator(listening, 25)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'listening/listening_list.html', {'page_obj': page_obj})

@teacher_required
def listening_detail(request, pk):
    listening = get_object_or_404(models.Listening, pk=pk)

    images = {img.caption: img.image_file.url for img in listening.images.all()}
    
    question = text_to_html.convert(listening.question or '', images)

    return render(request, 'listening/listening_detail.html', {'listening' : listening, 'question' : question})

@student_required
def student_listening_view(request, group_pk, assignment_pk, task_pk):
    group = request.user.student_groups.get(pk=group_pk)
    assignment = group.assignment_distributions.get(pk=assignment_pk)
    task = assignment.assignment.listening_tasks.get(task_id=task_pk)
    listening = task.task

    if request.method == "POST":

        answers ={}
        for key, value in request.POST.items():
            if key.startswith("question"):
                answers[key] = value

        student_progress, _ = StudentProgress.objects.get_or_create(
            user=request.user,
            group=group,
            assignment=assignment,
        )

        ProgressListening.objects.update_or_create(
            progress=student_progress,
            listening_test=listening,
            defaults={'answers' : answers, 'submitted_at': timezone.now()}
        )

        return redirect("assignment:student_assignment_detail", group_pk=group.pk, assignment_pk=assignment_pk )

    images = {img.caption: img.image_file.url for img in listening.images.all()}

    question = text_to_html.convert(listening.question or '', images)

    return render(request, 'listening/student_listening_view.html', {'group' : group, 'listening' : listening, 'question' : question, 'assignment' : assignment})




class ListeningFormsetMixin:
    """Handles the create/update form + inline image formset together."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ListeningImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["image_formset"] = ListeningImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context["image_formset"]

        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            return super().form_valid(form)

        return self.render_to_response(self.get_context_data(form=form))


class ListeningCreateView(TeacherRequiredMixin, ListeningFormsetMixin, CreateView):
    model = Listening
    form_class = ListeningForm
    template_name = "listening/listening_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if response.status_code == 302:
            messages.success(self.request, f'"{self.object.title}" was created.')
        return response

    def get_success_url(self):
        return reverse("listening:listening_detail", kwargs={"pk": self.object.pk})


class ListeningUpdateView(TeacherRequiredMixin, ListeningFormsetMixin, UpdateView):
    model = Listening
    form_class = ListeningForm
    template_name = "listening/listening_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        if response.status_code == 302:
            messages.success(self.request, f'"{self.object.title}" was updated.')
        return response

    def get_success_url(self):
        return reverse("listening:listening_detail", kwargs={"pk": self.object.pk})


class ListeningDeleteView(TeacherRequiredMixin, DeleteView):
    model = Listening
    template_name = "listening/listening_confirm_delete.html"
    success_url = reverse_lazy("listening:listening_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["confirm_form"] = DeleteConfirmForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        confirm_form = DeleteConfirmForm(request.POST, user=request.user)

        if confirm_form.is_valid():
            title = self.object.title
            self.object.delete()
            messages.success(request, f'"{title}" was deleted.')
            return redirect(self.success_url)

        context = self.get_context_data(confirm_form=confirm_form)
        return self.render_to_response(context)