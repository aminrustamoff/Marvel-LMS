from django import forms
from django.forms import inlineformset_factory
from .models import ReadingArticle, ReadingArticleImage


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