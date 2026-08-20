from django.urls import path

from reading import article_views

app_name = "article"

urlpatterns = [
    path("", article_views.article_list, name="article_list"),
    path("details/<int:pk>/", article_views.article_detail, name="article_detail"),
    path("student/details/<int:assignment_pk>/<int:pk>/", article_views.student_article_view, name="student_article_view"),    
    path("student/details/<int:assignment_pk>/<int:pk>/mark-as-read", article_views.mark_as_read, name="mark_as_read"),    
    
    path("articles/create/", article_views.ReadingArticleCreateView.as_view(), name="article_create"),
    path("articles/<int:pk>/edit/", article_views.ReadingArticleUpdateView.as_view(), name="article_update"),
    path("articles/<int:pk>/delete/", article_views.ReadingArticleDeleteView.as_view(), name="article_delete"),

]