from django import forms

from .models import Group
from accounts.models import User  # sizdagi joylashuvga qarab import yo'lini moslang

INPUT_ATTRS = {"class": "form-control"}


class GroupForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role=User.Role.STUDENT).order_by(
            "first_name", "last_name"
        ),
        required=False,
        widget=forms.SelectMultiple(attrs={"id": "id_members", "class": "member-select"}),
    )

    class Meta:
        model = Group
        fields = ["name", "description", "members"]
        widgets = {
            "name": forms.TextInput(attrs=INPUT_ATTRS),
            "description": forms.Textarea(attrs={**INPUT_ATTRS, "rows": 3}),
        }