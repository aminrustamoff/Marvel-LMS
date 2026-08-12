from django.urls import path
from . import views

app_name = "assignment"

urlpatterns = [
    path("", views.assignment_list, name="assignment_list"),
    path("detail/<int:pk>/", views.assignment_detail, name="assignment_detail"),
    path("student/detail/<int:pk>/", views.student_assignment_detail, name="student_assignment_detail"),
]