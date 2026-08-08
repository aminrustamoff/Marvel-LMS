from django.conf import settings
from django.db import models


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    article = models.ForeignKey(
        "reading.ReadingArticle",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assignments",
    )
    reading_passage = models.ForeignKey(
        "reading.ReadingPassage",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assignments",
    )
    listening = models.ForeignKey(
        "listening.Listening",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assignments",
    )
    video = models.ForeignKey(
        "videos.ListeningPodcast",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="assignments",
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={"role": "TEACHER"},
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_assignments",
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
