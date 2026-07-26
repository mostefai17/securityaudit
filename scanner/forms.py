from django import forms


class WebsiteForm(forms.Form):
    website = forms.URLField(
        label='your website',
        widget=forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        error_messages={'invalid': 'Please enter a valid URL.'},
    )
