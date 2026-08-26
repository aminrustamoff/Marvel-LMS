from django.urls import path

from . import views

app_name = "progress"

urlpatterns = [
    path("<int:group_pk>/<int:assignment_pk>/", views.student_assignment_progress_view, name="table_view"),

]
