from django.conf import settings
from django.db import models
from django.utils import timezone


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={"role": "TEACHER"},
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_assignments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class AssignmentDistribution(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="distributions",
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="assignment_distributions",
    )

    due_date = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Assignment Distribution"
        verbose_name_plural = "Assignment Distributions"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "group"],
                name="unique_assignment_group_distribution",
            )
        ]

    def __str__(self):
        return f"{self.assignment.title} - {self.group} - {self.due_date}"

    def is_expired(self):
        if not self.due_date:
            return False

        return self.due_date < timezone.localdate()

    def is_done(self, user, group):
        progress = self.student_progress.filter(user=user, group=group).first()

        if not progress:
            return False

        for assignment_task in self.assignment.article_tasks.all():
            if not progress.article_progress.filter(
                article=assignment_task.task,
                is_read=True
            ).exists():
                return False

        for assignment_task in self.assignment.passage_tasks.all():
            if not progress.reading_progress.filter(
                passage=assignment_task.task,
                submitted_at__isnull=False
            ).exists():
                return False

        for assignment_task in self.assignment.listening_tasks.all():
            if not progress.listening_progress.filter(
                listening_test=assignment_task.task,
                submitted_at__isnull=False
            ).exists():
                return False

        for assignment_task in self.assignment.podcast_tasks.all():
            if not progress.podcast_progress.filter(
                podcast=assignment_task.task,
                is_seen=True
            ).exists():
                return False

        return True

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