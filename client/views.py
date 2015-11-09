from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    context = {
    'apiUrl': request.build_absolute_uri(reverse('core:api-root')),
    'baseUrl': reverse('client:index'),
    }
    return render (request, 'index.html', {'context': context})
