from django.contrib import admin
from .models import ListeningPodcast

@admin.register(ListeningPodcast)
class ListeningPodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_by', 'created_at')
    search_fields = ('title', 'description', 'url')
    list_filter = ('created_by', 'created_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.created_by is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

