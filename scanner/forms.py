from django import forms


class WebsiteForm(forms.Form):
    website = forms.URLField(
        label = "your website",
        placeholders = "https://examples.come",
        error_messages = {'invalid': 'Please enter a valid URL.'}
    )
