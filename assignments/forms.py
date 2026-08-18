from django import forms

from listening.models import Listening
from reading.models import ReadingArticle, ReadingPassage
from videos.models import ListeningPodcast

from .models import Assignment

INPUT_ATTRS = {"class": "form-control"}


class AssignmentForm(forms.ModelForm):
    articles = forms.ModelMultipleChoiceField(
        queryset=ReadingArticle.objects.order_by("title"),
        required=False,
        widget=forms.SelectMultiple(attrs={"id": "id_articles", "class": "task-select"}),
    )
    passages = forms.ModelMultipleChoiceField(
        queryset=ReadingPassage.objects.order_by("title"),
        required=False,
        widget=forms.SelectMultiple(attrs={"id": "id_passages", "class": "task-select"}),
    )
    listenings = forms.ModelMultipleChoiceField(
        queryset=Listening.objects.order_by("title"),
        required=False,
        widget=forms.SelectMultiple(attrs={"id": "id_listenings", "class": "task-select"}),
    )
    podcasts = forms.ModelMultipleChoiceField(
        queryset=ListeningPodcast.objects.order_by("title"),
        required=False,
        widget=forms.SelectMultiple(attrs={"id": "id_podcasts", "class": "task-select"}),
    )

    class Meta:
        model = Assignment
        fields = ["title", "description", "groups", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs=INPUT_ATTRS),
            "description": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 3}),
            "groups": forms.SelectMultiple(attrs={"id": "id_groups", "class": "task-select"}),
            "due_date": forms.DateInput(attrs={**INPUT_ATTRS, "type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On update, pre-select the currently linked tasks so the form shows existing state.
        if self.instance.pk:
            self.fields["articles"].initial = self.instance.article_tasks.values_list("task_id", flat=True)
            self.fields["passages"].initial = self.instance.passage_tasks.values_list("task_id", flat=True)
            self.fields["listenings"].initial = self.instance.listening_tasks.values_list("task_id", flat=True)
            self.fields["podcasts"].initial = self.instance.podcast_tasks.values_list("task_id", flat=True)