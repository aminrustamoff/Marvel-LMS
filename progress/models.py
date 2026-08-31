from django.db import models
from django.conf import settings

from assignments.models import Assignment, AssignmentDistribution
from groups.models import Group
from reading.models import ReadingPassage, ReadingArticle # sizning haqiqiy nomingizga moslang
from videos.models import ListeningPodcast
from listening.models import Listening  # sizning haqiqiy nomingizga moslang


class StudentProgress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={"role": "STUDENT"},
        on_delete=models.CASCADE,
        related_name="progress_records",
    )
    group = models.ForeignKey(
        Group,
        null=True,
        on_delete=models.SET_NULL,
        related_name="progress_groups",
    )
    assignment = models.ForeignKey(
        AssignmentDistribution,
        null=True,
        on_delete=models.SET_NULL,
        related_name="student_progress",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "group", "assignment")

    def __str__(self):
        return f"{self.user} — {self.group} — {self.assignment}"


class ProgressArticle(models.Model):
    progress = models.ForeignKey(
        StudentProgress, on_delete=models.CASCADE, related_name="article_progress"
    )
    article = models.ForeignKey(ReadingArticle, on_delete=models.CASCADE)

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("progress", "article")


class ProgressReading(models.Model):
    progress = models.ForeignKey(
        StudentProgress, on_delete=models.CASCADE, related_name="reading_progress"
    )
    passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE)

    answers = models.JSONField(default=dict, blank=True)
    score = models.FloatField(null=True, blank=True)

    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("progress", "passage")


class ProgressPodcast(models.Model):
    progress = models.ForeignKey(
        StudentProgress, on_delete=models.CASCADE, related_name="podcast_progress"
    )
    podcast = models.ForeignKey(ListeningPodcast, on_delete=models.CASCADE)

    is_seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("progress", "podcast")


class ProgressListening(models.Model):
    progress = models.ForeignKey(
        StudentProgress, 
        on_delete=models.CASCADE, 
        related_name="listening_progress"
    )
    listening_test = models.ForeignKey(
        Listening, 
        on_delete=models.CASCADE,
    )

    answers = models.JSONField(default=dict, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("progress", "listening_test")