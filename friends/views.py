from django.shortcuts import render
from django.http import HttpResponse


from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework import generics

from django.shortcuts import render
from .serializers import FriendSerializer, FriendshipRequestSerializer
from core.serializers import UserSerializer
from .models import Friend

# Create your views here.

class FriendshipRequestViewSet(viewsets.ViewSet):
    """
        FriendshipRequest viewset
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipRequestSerializer

    def create(self, request):
        """ create a friendship request """
        #we add the request in the context of the serializer
        serializer = self.serializer_class(data = request.data)


        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)


        return Response({
            'status': 'Bad request',
            'message': 'Friendship request could not be sent :('
        }, status=status.HTTP_400_BAD_REQUEST)



class FriendViewSet(viewsets.ViewSet):
    """
    friend View Set
    """
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendSerializer

    def list(self, request):
        """List friends of authenticated user"""

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

    # def create(self, request):
    #     """ cannot create friends directly, need to pass by a request """
    #     pass
