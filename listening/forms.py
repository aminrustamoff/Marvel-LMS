from django import forms
from django.forms import inlineformset_factory

from .models import Listening, ListeningImages

INPUT_ATTRS = {"class": "form-control"}


class ListeningForm(forms.ModelForm):
    class Meta:
        model = Listening
        fields = ["title", "part", "question", "answer", "audio_file"]
        widgets = {
            "title": forms.TextInput(attrs=INPUT_ATTRS),
            "part": forms.Select(attrs=INPUT_ATTRS),
            "question": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 6}),
            "answer": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 4}),
            "audio_file": forms.FileInput(attrs={"class": "form-control-file", "accept": "audio/*"}),
        }


class ListeningImageForm(forms.ModelForm):
    class Meta:
        model = ListeningImages
        fields = ["caption", "image_file"]
        widgets = {
            "caption": forms.TextInput(attrs={**INPUT_ATTRS, "placeholder": "Optional caption"}),
            "image_file": forms.FileInput(attrs={"class": "form-control-file", "accept": "image/*"}),
        }


ListeningImageFormSet = inlineformset_factory(
    Listening,
    ListeningImages,
    form=ListeningImageForm,
    extra=1,
    can_delete=True,
)


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