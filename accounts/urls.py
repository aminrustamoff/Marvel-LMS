from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import (
    RoleBasedLoginView,
    student_list,
    student_detail,
    teacher_list,
    teacher_detail,
    UserCreateView,
    UserUpdateView,
    password_reset,
    UserDeleteView
)

app_name = "accounts"

urlpatterns = [
    path("login/", RoleBasedLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("students/", student_list, name="student_list"),
    path("students/<int:pk>/", student_detail, name="student_detail"),

    path("teachers/", teacher_list, name="teacher_list"),
    path("teachers/<int:pk>/", teacher_detail, name="teacher_detail"),

    path("create-user/", UserCreateView.as_view(), name="create_user"),
    path("<int:pk>/update-user/", UserUpdateView.as_view(), name="update_user"),
    path("<int:pk>/reset-password/", password_reset, name="password_reset"),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]