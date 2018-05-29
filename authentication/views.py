from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from djoser import utils, serializers, signals
from djoser.conf import settings

from .serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()

class RegistrationView(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data = request.data, context={'request':request})

        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.validated_data.get('email'))
            token = utils.login_user(self.request, user)
            token_serializer_class = settings.SERIALIZERS.token
            return Response(
                data=token_serializer_class(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request):
        if request.user.is_anonymous:
            return Response({
                'message': 'You are Anonymous',
            }, status=status.HTTP_200_OK)

        serializer = self.serializer_class(request.user, many=False, context= { 'request': request })
        return Response(serializer.data, status=status.HTTP_200_OK)
