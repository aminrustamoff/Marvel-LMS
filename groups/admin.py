from django.contrib import admin

from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "member_count", "created_at")
    search_fields = ("name",)
    filter_horizontal = ("members",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "description", "members")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
