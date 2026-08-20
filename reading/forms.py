from django import forms
from django.forms import inlineformset_factory
from .models import ReadingArticle, ReadingArticleImage, ReadingPassage, ReadingPassageImage


class ReadingArticleForm(forms.ModelForm):
    class Meta:
        model = ReadingArticle
        fields = ["title", "subtitle", "cover", "content"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Title"
            }),
            "subtitle": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Short subtitle (optional)"
            }),
            "cover": forms.ClearableFileInput(attrs={
                "class": "form-file-input",
                "accept": "image/*"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-textarea",
                "rows": 12,
                "placeholder": "Article text..."
            }),
        }


class ReadingArticleImageForm(forms.ModelForm):
    class Meta:
        model = ReadingArticleImage
        fields = ["image", "caption"]
        widgets = {
            "image": forms.ClearableFileInput(attrs={
                "class": "form-file-input",
                "accept": "image/*"
            }),
            "caption": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Image caption (optional)"
            }),
        }


# Bitta maqolaga bog'liq bir nechta rasm uchun formset
ReadingArticleImageFormSet = inlineformset_factory(
    ReadingArticle,
    ReadingArticleImage,
    form=ReadingArticleImageForm,
    extra=1,
    can_delete=True,
)


class DeleteConfirmForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Enter your password...",
            "autocomplete": "current-password",
        }),
        label="Password",
    )


from django import forms
from django.forms import inlineformset_factory

from .models import ReadingPassage, ReadingPassageImage

INPUT_ATTRS = {"class": "form-control"}


class ReadingPassageForm(forms.ModelForm):
    class Meta:
        model = ReadingPassage
        fields = ["title", "subtitle", "passage", "image", "passage_text", "question_text", "answers"]
        widgets = {
            "title": forms.TextInput(attrs=INPUT_ATTRS),
            "subtitle": forms.TextInput(attrs=INPUT_ATTRS),
            "passage": forms.Select(attrs=INPUT_ATTRS),
            "image": forms.FileInput(attrs={"class": "form-control-file", "accept": "image/*"}),
            "passage_text": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 10}),
            "question_text": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 8}),
            "answers": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 4}),
        }


class ReadingPassageImageForm(forms.ModelForm):
    class Meta:
        model = ReadingPassageImage
        fields = ["caption", "image"]
        widgets = {
            "caption": forms.TextInput(attrs={**INPUT_ATTRS, "placeholder": "Optional caption"}),
            "image": forms.FileInput(attrs={"class": "form-control-file", "accept": "image/*"}),
        }


ReadingPassageImageFormSet = inlineformset_factory(
    ReadingPassage,
    ReadingPassageImage,
    form=ReadingPassageImageForm,
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