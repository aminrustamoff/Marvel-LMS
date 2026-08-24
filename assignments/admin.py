from django.contrib import admin

from .models import ArticleTask, Assignment, ListeningTask, PassageTask, PodcastTask

class ArticleTaskInline(admin.TabularInline):
    model = ArticleTask
    extra = 1

class PassageTaskInline(admin.TabularInline):
    model = PassageTask
    extra = 1

class ListeningTaskInline(admin.TabularInline):
    model = ListeningTask
    extra = 1

class PodcastTaskInline(admin.TabularInline):
    model = PodcastTask
    extra = 1
    



@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_by", "created_at")
    list_filter = ( "assigned_by",)
    search_fields = ("title", "description")
    inlines = (ArticleTaskInline, PassageTaskInline, ListeningTaskInline, PodcastTaskInline)
    readonly_fields = ("assigned_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk or obj.assigned_by is None:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)
