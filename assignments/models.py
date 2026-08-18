from django.conf import settings
from django.db import models


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    groups = models.ManyToManyField(
        "groups.Group",
        related_name="assignments",
        blank=True,
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

class ArticleTask(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="article_tasks",
    )

    task = models.ForeignKey(
        "reading.ReadingArticle",
        on_delete=models.CASCADE,
        related_name="article_tasks",
    )
    
    class Meta:
        verbose_name = "Assignment Task"
        verbose_name_plural = "Assignment Tasks"
        unique_together = ("assignment", "task")

    def __str__(self):
        return f"{self.assignment.title} - {self.task.title}"

class PassageTask(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="passage_tasks",
    )

    task = models.ForeignKey(
        "reading.ReadingPassage",
        on_delete=models.CASCADE,
        related_name="passage_tasks",
    )
    
    class Meta:
        verbose_name = "Assignment Task"
        verbose_name_plural = "Assignment Tasks"
        unique_together = ("assignment", "task")

    def __str__(self):
        return f"{self.assignment.title} - {self.task.title}"

class ListeningTask(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="listening_tasks",
    )

    task = models.ForeignKey(
        "listening.Listening",
        on_delete=models.CASCADE,
        related_name="listening_tasks",
    )
    
    class Meta:
        verbose_name = "Assignment Task"
        verbose_name_plural = "Assignment Tasks"
        unique_together = ("assignment", "task")

    def __str__(self):
        return f"{self.assignment.title} - {self.task.title}"

class PodcastTask(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="podcast_tasks",
    )

    task = models.ForeignKey(
        "videos.ListeningPodcast",
        on_delete=models.CASCADE,
        related_name="podcast_tasks",
    )
    
    class Meta:
        verbose_name = "Assignment Task"
        verbose_name_plural = "Assignment Tasks"
        unique_together = ("assignment", "task")

    def __str__(self):
        return f"{self.assignment.title} - {self.task.title}"