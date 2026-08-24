from django.urls import path
from . import views

app_name = "listening"

urlpatterns = [
    path("", views.listening_list, name="listening_list"),
    path("details/<int:pk>/", views.listening_detail, name="listening_detail"),
    path("student/details/<int:group_pk>/<int:assignment_pk>/<int:task_pk>/", views.student_listening_view, name="student_listening_view"),

    path("create/", views.ListeningCreateView.as_view(), name="listening_create"),
    path("<int:pk>/update/", views.ListeningUpdateView.as_view(), name="listening_update"),
    path("<int:pk>/delete/", views.ListeningDeleteView.as_view(), name="listening_delete"),
]

