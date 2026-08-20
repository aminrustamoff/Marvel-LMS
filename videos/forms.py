from django import forms

from .models import ListeningPodcast

INPUT_ATTRS = {"class": "form-control"}


class ListeningPodcastForm(forms.ModelForm):
    class Meta:
        model = ListeningPodcast
        fields = ["title", "description", "url"]
        widgets = {
            "title": forms.TextInput(attrs=INPUT_ATTRS),
            "description": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 4}),
            "url": forms.URLInput(attrs={**INPUT_ATTRS, "placeholder": "https://youtube.com/watch?v=..."}),
        }


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