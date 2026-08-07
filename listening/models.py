from django.conf import settings
from django.db import models

class Listening(models.Model):
    PART_CHOICES = [
        ("Part 1", "Part 1"),
        ("Part 2", "Part 2"),
        ("Part 3", "Part 3"),
        ("Part 4", "Part 4"),
    ]

    title = models.CharField(max_length=200)
    part = models.CharField(max_length=6, choices=PART_CHOICES, default="Part 1")

    question = models.TextField()
    answer = models.TextField()

    audio_file = models.FileField(upload_to='listening/audio/')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="listening_created",
        limit_choices_to={"role": "TEACHER"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.part})"


class ListeningImages(models.Model):
    listening = models.ForeignKey(Listening, on_delete=models.CASCADE, related_name='images')
    caption = models.CharField(max_length=200, blank=True)
    image_file = models.ImageField(upload_to='listening/images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listening.title}"

