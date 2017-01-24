from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    API_URL = request.build_absolute_uri(reverse('api-root'))
    BASE_URL = '/client'
    return render (request, 'client/index.html', {'API_URL': API_URL, 'BASE_URL': BASE_URL})
