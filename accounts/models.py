from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        TEACHER = "TEACHER", "Teacher"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    active_until = models.DateField(
        null=True,
        blank=True,
        help_text="If empty, there will be no limit to access.",
    )

    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    email = models.EmailField(blank=True)

    def is_teacher(self):
        return self.role == self.Role.TEACHER

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_expired(self):
        return bool(self.active_until) and self.active_until < timezone.localdate()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"