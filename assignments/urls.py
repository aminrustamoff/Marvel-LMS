from django.urls import path
from . import views

app_name = "assignment"

urlpatterns = [
    path("", views.assignment_list, name="assignment_list"),
    path("detail/<int:pk>/", views.assignment_detail, name="assignment_detail"),
    path("student/detail/<int:pk>/", views.student_assignment_detail, name="student_assignment_detail"),

    path("create/", views.AssignmentCreateView.as_view(), name="assignment_create"),
    path("<int:pk>/update/", views.AssignmentUpdateView.as_view(), name="assignment_update"),
    path("<int:pk>/delete/", views.AssignmentDeleteView.as_view(), name="assignment_delete"),
]