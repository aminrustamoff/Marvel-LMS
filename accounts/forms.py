from django import forms
from django.contrib.auth import get_user_model, authenticate 
from django.utils.crypto import get_random_string
from . import models

User = get_user_model()

INPUT_ATTRS = {'class': 'input-field'}


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'role', 'is_active', 'active_until', 'phone_number', 'email', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs=INPUT_ATTRS),
            'last_name': forms.TextInput(attrs=INPUT_ATTRS),
            'username': forms.TextInput(attrs=INPUT_ATTRS),
            'role': forms.Select(attrs=INPUT_ATTRS),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle-input'}),
            'active_until': forms.DateInput(
                            attrs={**INPUT_ATTRS, "type": "date"},
                            format="%Y-%m-%d",
                        ),
            'phone_number': forms.TextInput(attrs=INPUT_ATTRS),
            'email': forms.EmailInput(attrs=INPUT_ATTRS),
            'avatar': forms.ClearableFileInput(attrs={'class': 'file-input'}),
        }


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs=INPUT_ATTRS),
        required=False,  # left blank → auto-generated
        help_text="If you leave this empty, the password will be generated automatically."
    )

    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'username', 'role', 'is_active', 'active_until', 'phone_number', 'email', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs=INPUT_ATTRS),
            'last_name': forms.TextInput(attrs=INPUT_ATTRS),
            'username': forms.TextInput(attrs=INPUT_ATTRS),
            'role': forms.Select(attrs=INPUT_ATTRS),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle-input'}),
            'active_until': forms.DateInput(
                attrs={**INPUT_ATTRS, "type": "date"},
                format="%Y-%m-%d",
            ),
            'phone_number': forms.TextInput(attrs=INPUT_ATTRS),
            'email': forms.EmailInput(attrs=INPUT_ATTRS),
            'avatar': forms.ClearableFileInput(attrs={'class': 'file-input'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password1')
        if not password:
            password = get_random_string(
                length=8,
                allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'  # skips confusing chars (0/O, 1/l)
            )
            self.generated_password = password  # shown once after save, never stored in plaintext

        user.set_password(password)  # ← never assign user.password directly

        if commit:
            user.save()
        return user

class AdminPasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'input-field'}),
        min_length=6,
    )
    new_password2 = forms.CharField(
        label="Verify Password",
        widget=forms.PasswordInput(attrs={'class': 'input-field'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password1')
        p2 = cleaned_data.get('new_password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data




class UserDeleteConfirmForm(forms.Form):
    password = forms.CharField(
        label="Your password",
        widget=forms.PasswordInput(attrs={'class': 'input-field'}),
        help_text="Enter your own password to confirm this action."
    )

    def __init__(self, *args, request_user=None, **kwargs):
        self.request_user = request_user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']
        # request_user — o'chirishni amalga oshirayotgan teacher/admin, o'chirilayotgan user emas
        user = authenticate(username=self.request_user.username, password=password)
        if user is None:
            raise forms.ValidationError("Incorrect password. Please try again.")
        return password