from django.urls import path

from . import views

app_name = "reading"

urlpatterns = [
    path("", views.reading_list, name="reading_list"),
    path("details/<int:pk>/", views.reading_detail, name="reading_detail"),
    path("student/details/<int:assignment_pk>/<int:pk>/", views.student_reading_test_view, name="student_reading_view"),
    path("student/details/<int:assignment_pk>/<int:pk>/submit", views.submit_answers, name="submit_answers"),
    path("student/details/<int:pk>/result", views.student_reading_result, name="result"),
]