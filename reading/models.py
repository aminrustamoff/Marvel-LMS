from django.conf import settings
from django.db import models


# ============================================================
# 1) READING ARTICLE — faqat matn, savol yo'q, faqat highlight/note
# ============================================================

class ReadingArticle(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="reading/articles/", null=True, blank=True)

    content = models.TextField(help_text="Maqola matni (oddiy text yoki paragraflar)")
    # An article can have multiple images; use a separate model ReadingArticleImage
    # to store multiple ImageField instances related to this article.

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_articles",
        limit_choices_to={"role": "TEACHER"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.subtitle})"


class ReadingArticleImage(models.Model):
    article = models.ForeignKey(
        ReadingArticle, on_delete=models.CASCADE, related_name="images"
    )

    image = models.ImageField(upload_to="reading/articles/")
    caption = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.article.title} ({self.id})"


# ============================================================
# 2) READING PASSAGE — matn + savollar
# ============================================================

class ReadingPassage(models.Model):

    PART_CHOICES = [
            ("Passage 1", "Passage 1"),
            ("Passage 2", "Passage 2"),
            ("Passage 3", "Passage 3"),
        ]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    passage = models.CharField(max_length=50, choices=PART_CHOICES, default="Passage 1")
    image = models.ImageField(upload_to="reading/passages/", null=True, blank=True)

    passage_text = models.TextField()
    question_text = models.TextField()
    answers = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_passages",
        limit_choices_to={"role": "TEACHER"},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.passage})"

class ReadingPassageImage(models.Model):
    passage = models.ForeignKey(
        ReadingPassage, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="reading/passages/")
    caption = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.passage.title} ({self.id})"