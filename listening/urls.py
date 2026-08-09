from django.urls import path
from . import views

app_name = "listening"

urlpatterns = [
    path("", views.listening_list, name="listening_list"),
    path("details/<int:pk>/", views.listening_detail, name="listening_detail"),
]

