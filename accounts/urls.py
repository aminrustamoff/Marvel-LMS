from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import (
    RoleBasedLoginView,
    student_list,
    student_detail,
    teacher_list,
    teacher_detail,
)

app_name = "accounts"

urlpatterns = [
    path("login/", RoleBasedLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("students/", student_list, name="student_list"),
    path("students/<int:pk>/", student_detail, name="student_detail"),

    path("teachers/", teacher_list, name="teacher_list"),
    path("teachers/<int:pk>/", teacher_detail, name="teacher_detail")
]