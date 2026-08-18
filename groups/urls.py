from django.urls import path

from . import views

app_name = "groups"

urlpatterns = [
    path("", views.group_list, name="list"),
    path("detail/<int:pk>/", views.group_detail, name="detail"),
    path("student/detail/<int:pk>/", views.student_group_detail, name="student_detail"),

    path("create/", views.GroupCreateView.as_view(), name="group_create"),
    path("<int:pk>/update/", views.GroupUpdateView.as_view(), name="group_update"),
    path("<int:pk>/delete/", views.GroupDeleteView.as_view(), name="group_delete"),
]
