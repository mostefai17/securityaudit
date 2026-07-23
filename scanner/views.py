from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import WebsiteForm
from urllib.parse import urlsplit
import requests
# Create your views here.

def get_website_name(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        
        if form.is_valid():

            website = WebsiteForm.cleaned_data['website']
            website_name = urlsplit(website).netloc
            return HttpResponseRedirect('success')

        else:
            form = WebsiteForm()
        return render(request, 'name.html', {'form': form})