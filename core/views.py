from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from serializers import UserSerializer

from rest_framework.response import Response
from rest_framework import status, permissions, viewsets

User = get_user_model()

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the core index.")

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
