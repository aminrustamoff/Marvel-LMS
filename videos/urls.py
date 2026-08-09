from django.urls import path
from . import views

app_name = "podcast"

urlpatterns = [
    path("", views.video_list, name="video_list"),
    path("detail/<int:pk>/", views.video_detail, name="video_detail"),
]