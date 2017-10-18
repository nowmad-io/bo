from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from djoser import utils, serializers, signals

from .serializers import UserRegisterSerializer

User = get_user_model()

class RegistrationView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
