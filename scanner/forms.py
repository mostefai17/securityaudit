from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class WebsiteForm(forms.Form):
    website = forms.URLField(
        label="your website",
        widget=forms.URLInput(attrs={"placeholder": "https://example.com"}),
        error_messages={"invalid": "Please enter a valid URL."},
    )


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")
