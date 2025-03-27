import random
import string

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import Url
from .models import UrlData


def index(request):
    return HttpResponse("Hello World")

def url_short(request):
    if request.method == 'POST':
        form = Url(request.POST)
        if form.is_valid():
            slug = ''.join(random.choice(string.ascii_letters)
                           for x in range(10))
            url = form.cleaned_data["url"]
            if request.user.is_authenticated:
                new_url = UrlData(url=url, slug=slug, user=request.user)
                new_url.save()
            else:
                new_url = UrlData(url=url, slug=slug)
                new_url.save()
                data = [new_url]
                context = {
                    'form': form,
                    'data': data
                }
                return render(request, 'url/index.html', context)


            return redirect('/')
    else:
        form = Url()

    if request.user.is_authenticated:
        data = UrlData.objects.filter(user=request.user)
    else:
        data = {}
    context = {
        'form': form,
        'data': data
    }
    return render(request, 'url/index.html', context)


def url_redirect(request, slugs):
    data = get_object_or_404(UrlData, slug=slugs)
    url = data.url

    # Ensure the URL has a scheme (http/https)
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Default to HTTPS

    return HttpResponseRedirect(url)