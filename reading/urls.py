from django.urls import path

from . import views

app_name = "reading"

urlpatterns = [
    path("", views.reading_list, name="reading_list"),
    path("details/<int:pk>/", views.reading_detail, name="reading_detail"),
    path("student/details/<int:group_pk>/<int:assignment_pk>/<int:task_pk>/", views.student_reading_test_view, name="student_reading_view"),

    path("passages/create/", views.ReadingPassageCreateView.as_view(), name="reading_create"),
    path("passages/<int:pk>/update/", views.ReadingPassageUpdateView.as_view(), name="reading_update"),
    path("passages/<int:pk>/delete/", views.ReadingPassageDeleteView.as_view(), name="reading_delete"),
]