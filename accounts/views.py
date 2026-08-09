from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from accounts.models import User


class RoleBasedLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to

        if self.request.user.role == User.Role.TEACHER:
            return reverse("dashboard:teacher_dashboard")
        return reverse("dashboard:student_dashboard")


@login_required
def student_list(request):
    students = User.objects.filter(role=User.Role.STUDENT)
    return render(request, "accounts/student_list.html", {"students": students})


@login_required
def student_detail(request, pk):
    student = User.objects.get(pk=pk, role=User.Role.STUDENT)
    return render(request, "accounts/student_detail.html", {"student": student})


@login_required
def teacher_list(request):
    teachers = User.objects.filter(role=User.Role.TEACHER)
    return render(request, "accounts/teacher_list.html", {"teachers": teachers})


@login_required
def teacher_detail(request, pk):
    teacher = User.objects.get(pk=pk, role=User.Role.TEACHER)
    return render(request, "accounts/teacher_detail.html", {"teacher": teacher})