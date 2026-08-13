from django.db import models
from django.core.validators import URLValidator

from config import settings

class ListeningPodcast(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    url = models.URLField(validators=[URLValidator()])

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="listening_podcast_created",
        limit_choices_to={"role": "TEACHER"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title}"
