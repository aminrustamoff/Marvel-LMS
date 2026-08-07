from django.contrib import admin
from .models import Listening, ListeningImages


class ListeningImagesInline(admin.TabularInline):
    model = ListeningImages
    extra = 1


@admin.register(Listening)
class ListeningAdmin(admin.ModelAdmin):
    list_display = ("title", "part", "created_at")
    list_filter = ("part", "created_at")
    search_fields = ("title", "question", "answer")
    inlines = (ListeningImagesInline,)
