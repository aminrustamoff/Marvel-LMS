from django.urls import path
from . import views

app_name = "assignment"

urlpatterns = [
    path("", views.assignment_list, name="assignment_list"),
    path("detail/<int:pk>/", views.assignment_detail, name="assignment_detail"),
    path("student/detail/<int:group_pk>/<int:assignment_pk>/", views.student_assignment_detail, name="student_assignment_detail"),

    path("create/", views.AssignmentCreateView.as_view(), name="assignment_create"),
    path("<int:pk>/update/", views.AssignmentUpdateView.as_view(), name="assignment_update"),
    path("<int:pk>/delete/", views.AssignmentDeleteView.as_view(), name="assignment_delete"),

    path(
        "<int:assignment_pk>/distributions/create/",
        views.AssignmentDistributionCreateView.as_view(),
        name="assignment_distribution_create",
    ),
    path(
        "<int:assignment_pk>/distributions/<int:pk>/update/",
        views.AssignmentDistributionUpdateView.as_view(),
        name="assignment_distribution_update",
    ),
    path(
        "<int:assignment_pk>/distributions/<int:pk>/delete/",
        views.AssignmentDistributionDeleteView.as_view(),
        name="assignment_distribution_delete",
    ),
]