from django.contrib import admin
from .models import Listening, ListeningImages


class ListeningImagesInline(admin.TabularInline):
    model = ListeningImages
    extra = 1


@admin.register(Listening)
class ListeningAdmin(admin.ModelAdmin):
    list_display = ("title", "part", "created_by", "created_at", "updated_at")
    list_filter = ("part", "created_by", "created_at")
    search_fields = ("title", "question", "answer")
    inlines = (ListeningImagesInline,)
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.created_by is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
