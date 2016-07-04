from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from serializers import UserSerializer, ReviewSerializer
from models import Review

from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework import generics

User = get_user_model()

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the core index.")

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def perform_create(self, serializer):
        serializer.save()



class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        print 'blabla'
        print self.request.user.get_full_name()
        serializer.save()
