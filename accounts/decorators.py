from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps


def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url="accounts:login")
        def _wrapped(request, *args, **kwargs):
            if request.user.role != role:
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


teacher_required = role_required("TEACHER")
student_required = role_required("STUDENT")


# Class-based view uchun mixin:

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "accounts:login"

    def test_func(self):
        return self.request.user.role == "TEACHER"


'''
Foydalanish misoli — dashboard/views.py
python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = "accounts:login"
    template_name = "dashboard/dashboard.html"
'''