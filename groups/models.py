from django.conf import settings
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="student_groups",
        blank=True,
        limit_choices_to={"role": "STUDENT"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def member_count(self):
        return self.members.count()

    member_count.short_description = "Student count"
