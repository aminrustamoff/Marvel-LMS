from django.urls import path

from reading import article_views
from . import views

app_name = "article"

urlpatterns = [
    path("", article_views.article_list, name="article_list"),
    path("details/<int:pk>/", article_views.article_detail, name="article_detail")
]