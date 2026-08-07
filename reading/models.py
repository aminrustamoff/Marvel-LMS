from django.conf import settings
from django.db import models


# ============================================================
# 1) READING ARTICLE — faqat matn, savol yo'q, faqat highlight/note
# ============================================================

class ReadingArticle(models.Model):
    title = models.CharField(max_length=255)
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
        return self.title


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
    title = models.CharField(max_length=255)
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
        return self.title

class ReadingPassageImage(models.Model):
    passage = models.ForeignKey(
        ReadingPassage, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="reading/passages/")
    caption = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.passage.title} ({self.id})"


# # ============================================================
# # 3) HIGHLIGHT va NOTE — ikkalasi ham Article'ga ham Passage'ga tegishli bo'la oladi
# # ============================================================

# class Highlight(models.Model):
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="highlights")
#     article = models.ForeignKey(ReadingArticle, on_delete=models.CASCADE, null=True, blank=True, related_name="highlights")
#     passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, null=True, blank=True, related_name="highlights")

#     start_offset = models.PositiveIntegerField()
#     end_offset = models.PositiveIntegerField()
#     highlighted_text = models.TextField()
#     color = models.CharField(max_length=20, default="yellow")

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=(
#                     models.Q(article__isnull=False, passage__isnull=True)
#                     | models.Q(article__isnull=True, passage__isnull=False)
#                 ),
#                 name="highlight_belongs_to_one_source",
#             )
#         ]

#     def __str__(self):
#         return f"{self.student.username}: {self.highlighted_text[:30]}"


# class Note(models.Model):
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notes")
#     article = models.ForeignKey(ReadingArticle, on_delete=models.CASCADE, null=True, blank=True, related_name="notes")
#     passage = models.ForeignKey(ReadingPassage, on_delete=models.CASCADE, null=True, blank=True, related_name="notes")

#     content = models.TextField()
#     position = models.PositiveIntegerField(null=True, blank=True, help_text="Matn ichidagi taxminiy o'rin (offset)")

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 check=(
#                     models.Q(article__isnull=False, passage__isnull=True)
#                     | models.Q(article__isnull=True, passage__isnull=False)
#                 ),
#                 name="note_belongs_to_one_source",
#             )
#         ]

#     def __str__(self):
#         return f"{self.student.username}: {self.content[:30]}"