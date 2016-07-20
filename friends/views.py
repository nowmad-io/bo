from django.shortcuts import render
from django.http import HttpResponse


from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework import generics

from django.shortcuts import render
from .serializers import FriendSerializer
from core.serializers import UserSerializer
from .models import Friend

# Create your views here.




class FriendViewSet(viewsets.ViewSet):
    """
    Review View Set
    """
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = FriendSerializer

    def list(self, request):

        if request.user.is_authenticated():
            queryset = Friend.objects.friends(request.user)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Authentification required.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(queryset, many=True)
        print serializer.data
        return Response(serializer.data)

    def create(self, request):
        pass
