from django.contrib import admin

from .models import (
    ReadingArticle,
    ReadingArticleImage,
    ReadingPassage,
    ReadingPassageImage,
)


class ReadingArticleImageInline(admin.TabularInline):
    model = ReadingArticleImage
    extra = 1


class ReadingPassageImageInline(admin.TabularInline):
    model = ReadingPassageImage
    extra = 1


@admin.register(ReadingArticle)
class ReadingArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "created_by", "created_at", "updated_at")
    search_fields = ("title", "subtitle", "content")
    list_filter = ("created_by", "created_at")
    inlines = (ReadingArticleImageInline,)
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.created_by is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ReadingPassage)
class ReadingPassageAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle", "created_by", "created_at", "updated_at")
    search_fields = ("title", "subtitle", "passage_text", "question_text")
    list_filter = ("created_by", "created_at")
    inlines = (ReadingPassageImageInline,)
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.created_by is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
