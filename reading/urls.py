from django.urls import path

from . import views

app_name = "reading"

urlpatterns = [
    path("", views.reading_list, name="reading_list"),
    path("details/<int:pk>/", views.reading_detail, name="reading_detail")
]