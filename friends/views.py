from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework import generics

from django.shortcuts import render
from .serializers import FriendSerializer, FriendshipRequestSerializer
from core.serializers import UserSerializer
from .models import Friend, FriendshipRequest
import json
# Create your views here.

class FriendshipRequestViewSet(viewsets.ViewSet):
    """
        standard behaviour for friendship request
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipRequestSerializer

    def list(self, request):
        """ return the list of friendship request """
        pass

    def retrieve(self, request, pk):
        """ get info from the friendhsip request with pk = pk"""
        pass

    def destroy(self, request, pk):
        """ delete friendship request with pk=pk """
        friendship_request = get_object_or_404(FriendshipRequest,id=pk)

        if friendship_request.from_user.id != request.user.id:
            return Response({'message':'WhoAreYou ??'},  status=status.HTTP_403_FORBIDDEN)

        result = friendship_request.cancel()

        if result:
            return Response(status = status.HTTP_201_CREATED)

        return Response({
              'status': 'Bad request'
          }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        pass

    def create(self, request):
        """ create a friendship request """

        #chek if there is a from_user and a message
        if 'from_user' not in request.data:
            request.data['from_user']=request.user.id

        if 'message' not in request.data:
            request.data['message']= "come on, let\'s be friends !"

        #check the user performing the request is the user authenticated
        if request.data['from_user'] != request.user.id:
            return Response({'message':'WhoAreYou ??'},  status=status.HTTP_403_FORBIDDEN)



        #get the data back
        serializer = self.serializer_class(data = request.data)

        #build the request in the backend
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Friendship request could not be sent :('
        }, status=status.HTTP_400_BAD_REQUEST)

    def incoming_list(self, request):
        """ print the list of incoming transaction """
        queryset = Friend.objects.unrejected_requests(user = request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def outgoing_list(self, request):
        """List friends request of authenticated user"""
        queryset = Friend.objects.sent_requests(user = request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def accept(self, request, pk):
        """ accept a friendship request, create friend and remove the request form incoming"""

        friendship_request = get_object_or_404(FriendshipRequest,id=pk)

        if friendship_request.to_user.id != request.user.id:
            return Response({'message':'WhoAreYou ??'},  status=status.HTTP_403_FORBIDDEN)

        result = friendship_request.accept()

        if result:
            return Response(status = status.HTTP_201_CREATED)

        return Response({
              'status': 'Bad request'
          }, status=status.HTTP_400_BAD_REQUEST)


    def reject(self, request, pk):
        """ reject a friendship request """

        friendship_request = get_object_or_404(FriendshipRequest,id=pk)

        if friendship_request.to_user.id != request.user.id:
            return Response({'message':'WhoAreYou ??'},  status=status.HTTP_403_FORBIDDEN)

        result = friendship_request.reject()
        
        if result:
            return Response(status = status.HTTP_200_OK)

        return Response({
              'status': 'Bad request'
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

        return Response(serializer.data)

    def destroy(self, request):
        """Remove a friend"""
        pass

    # def create(self, request):
    #     """ cannot create friends directly, need to pass by a request """
    #     pass
