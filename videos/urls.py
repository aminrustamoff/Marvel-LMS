from django.urls import path
from . import views

app_name = "podcast"

urlpatterns = [
    path("", views.video_list, name="video_list"),
    path("detail/<int:pk>/", views.video_detail, name="video_detail"),
    path("student/detail/<int:group_pk>/<int:assignment_pk>/<int:task_pk>/", views.student_podcast_view, name="student_podcast_view"),

    path("create/", views.VideoCreateView.as_view(), name="video_create"),
    path("<int:pk>/update/", views.VideoUpdateView.as_view(), name="video_update"),
    path("<int:pk>/delete/", views.VideoDeleteView.as_view(), name="video_delete"),
]