from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("groups/", include("groups.urls")),
    path("dashboard/", include("dashboard.urls")),  # boshqa app'lar
    path("assignments/", include("assignments.urls")),
    path("listening/", include("listening.urls")),
    path("reading/", include("reading.urls")),
    path("articles/", include("reading.article_urls")),
    path("podcast/", include("videos.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)