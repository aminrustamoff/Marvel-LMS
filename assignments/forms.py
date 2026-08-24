from django import forms

from listening.models import Listening
from reading.models import ReadingArticle, ReadingPassage
from videos.models import ListeningPodcast
from groups.models import Group

from .models import Assignment, AssignmentDistribution

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
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs=INPUT_ATTRS),
            "description": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On update, pre-select the currently linked tasks so the form shows existing state.
        if self.instance.pk:
            self.fields["articles"].initial = self.instance.article_tasks.values_list("task_id", flat=True)
            self.fields["passages"].initial = self.instance.passage_tasks.values_list("task_id", flat=True)
            self.fields["listenings"].initial = self.instance.listening_tasks.values_list("task_id", flat=True)
            self.fields["podcasts"].initial = self.instance.podcast_tasks.values_list("task_id", flat=True)

class AssignmentDistributionForm(forms.ModelForm):   # <-- nom o'zgardi
    group = forms.ModelChoiceField(
        queryset=Group.objects.order_by("name"),
        widget=forms.Select(attrs={**INPUT_ATTRS, "id": "id_group"}),
    )

    class Meta:
        model = AssignmentDistribution   # <-- nom o'zgardi
        fields = ["group", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={**INPUT_ATTRS, "type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, assignment=None, **kwargs):
        self.assignment = assignment
        super().__init__(*args, **kwargs)

    def clean_group(self):
        group = self.cleaned_data["group"]
        qs = AssignmentDistribution.objects.filter(   # <-- nom o'zgardi
            assignment=self.assignment, group=group
        )
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This group is already assigned to this assignment.")
        return group


class DeleteConfirmForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={**INPUT_ATTRS, "autocomplete": "current-password"}),
        label="Confirm your password",
    )

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]
        if not self.user.check_password(password):
            raise forms.ValidationError("Incorrect password.")
        return password