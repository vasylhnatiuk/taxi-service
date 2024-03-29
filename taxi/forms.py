from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver


def check_license(license_number):
    if not len(license_number) == 8:
        raise ValidationError("License must consist of 8 charaters")

    elif not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters must be uppercase letters")

    elif not license_number[3:].isdigit():
        raise ValidationError("Last 5 characters must be digits")

    return license_number


class DriverCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "license_number", "first_name", "last_name"
        )

    def clean_license_number(self):
        return check_license(self.cleaned_data["license_number"])


class LicenseUpdateForm(forms.ModelForm):

    class Meta:
        model = Driver
        fields = ("license_number",)

    def clean_license_number(self):
        return check_license(self.cleaned_data["license_number"])


class CarSearchForm(forms.Form):
    model = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title..."})
    )




