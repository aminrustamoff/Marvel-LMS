from django.contrib import admin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "group", "assigned_by", "due_date", "created_at")
    list_filter = ("group", "assigned_by", "due_date")
    search_fields = ("title", "description")
    raw_id_fields = ("group", "article", "reading_passage", "listening", "video")
    readonly_fields = ("assigned_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.assigned_by is None:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)
