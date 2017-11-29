from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

from itertools import chain
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.shortcuts import render
from .serializers import FriendSerializer, FriendshipRequestSerializer, FriendSearchSerializer
from authentication.serializers import UserSerializer
from .models import Friend, FriendshipRequest
from sockets.views import FriendAccept, FriendCreate, FriendReject

import json
# Create your views here.

User = get_user_model()

class FriendshipRequestViewSet(viewsets.ViewSet):
    """
        standard behaviour for friendship request
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipRequestSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def list(self, request):
        """ return the list of friendship request """
        queryset = Friend.objects.requests(user = request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """ get info from the friendhsip request with pk = pk"""
        f_request = get_object_or_404(FriendshipRequest, id=pk)
        serializer = self.serializer_class(f_request)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """ delete friendship request with pk=pk """
        friendship_request = get_object_or_404(FriendshipRequest,id=pk)

        if friendship_request.from_user.id != request.user.id:
            return Response({
                'status': 'Forbidden',
                'message': 'Friends request can only destroy by current user.'
            }, status=status.HTTP_403_FORBIDDEN)

        result = friendship_request.cancel()

        if result:
            return Response(status = status.HTTP_201_CREATED)

        return Response({
              'status': 'Bad request'
          }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):

        friendship_request = get_object_or_404(FriendshipRequest,id=pk)

        if friendship_request.from_user.id != request.user.id:
            return Response({
                'status': 'Forbidden',
                'message': 'Friends request can only updated from current user.'
            }, status=status.HTTP_403_FORBIDDEN)


        serializer = self.serializer_class(friendship_request, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_202_ACCEPTED
            )

        return Response({
            'status': 'Bad request',
            'message': 'Review could not be created with received data.',
            'data': str(request.data),
            'validated_data': serializer.validated_data,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        """ create a friendship request """

        #chek if there is a from_user and a message
        if 'from_user_id' not in request.data:
            request.data['from_user_id']=request.user.id

        if 'message' not in request.data:
            request.data['message']= "come on, let\'s be friends !"

        #check the user performing the request is the user authenticated
        if int(request.data['from_user_id']) != request.user.id:
            return Response({
                'status': 'Forbidden',
                'message': 'Friends request can only created from current user.'
            }, status=status.HTTP_403_FORBIDDEN)

        #get the data back
        serializer = self.serializer_class(data = request.data, context={ 'request': request })

        #build the request in the backend
        if serializer.is_valid():
            serializer.save()

            friend = User.objects.get(pk=request.data['to_user_id'])
            FriendCreate([request.user, friend], serializer.data)

            return Response(status = status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Friendshipds could not be created with received data.',
            'data': str(request.data),
            'validated_data': serializer.validated_data,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def incoming_list(self, request):
        """ the list of incoming transaction """
        queryset = Friend.objects.unrejected_requests(user = request.user)
        serializer = self.serializer_class(queryset, many=True, context={ 'request': request })
        return Response(serializer.data)

    def outgoing_list(self, request):
        """List friends request of authenticated user"""
        queryset = Friend.objects.sent_requests(user = request.user)
        serializer = self.serializer_class(queryset, many=True, context={ 'request': request })
        return Response(serializer.data)

    def accept(self, request, pk):
        """ accept a friendship request, create friend and remove the request form incoming"""

        friendship_request = get_object_or_404(FriendshipRequest,id=pk)

        if friendship_request.to_user.id != request.user.id:
            return Response({
                'status': 'Forbidden',
                'message': 'Friends request can only sent from current user.'
            }, status=status.HTTP_403_FORBIDDEN)

        result = friendship_request.accept()

        if result:
            friend = User.objects.get(pk=friendship_request.from_user.id)
            serializer_friend = UserSerializer(friend, many=False, context={ 'request': request })
            serializer_user = UserSerializer(request.user, many=False, context={ 'request': request })
            FriendAccept(request.user, friend, serializer_user.data, serializer_friend.data)

            return Response(status = status.HTTP_201_CREATED)

        return Response({
              'status': 'Bad request'
          }, status=status.HTTP_400_BAD_REQUEST)


    def reject(self, request, pk):
        """ reject a friendship request """

        friendship_request = get_object_or_404(FriendshipRequest,id=pk)

        if friendship_request.to_user.id != request.user.id:
            return Response({
                'status': 'Forbidden',
                'message': 'Friends request can only be rejected by the current user.'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(friendship_request)
        result = friendship_request.reject()

        if result:
            friend = User.objects.get(pk=friendship_request.from_user.id)
            FriendReject([request.user, friend], serializer.data)
            return Response(status = status.HTTP_200_OK)

        return Response({
              'status': 'Bad request'
          }, status=status.HTTP_400_BAD_REQUEST)


class FriendViewSet(viewsets.ViewSet):
    """
    friend View Set
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def list(self, request):
        """List friends of authenticated user"""
        query = self.request.query_params.get('query', '')

        if request.user.is_authenticated():
            friendsId = list()
            friends = Friend.objects.friends(request.user)

            for friend in friends:
                friendsId.append(friend.id)
                friends_of_friend = Friend.objects.friends(friend)

                for friend_friend in friends_of_friend:
                    friendsId.append(friend_friend.id)

            queryset = User.objects.filter(
                pk__in=friendsId
            ).exclude(
                pk=request.user.id
            ).distinct()

        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Authentification required.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(queryset, many=True, context={ 'request': request })

        return Response(serializer.data)

    def destroy(self, request):
        """Remove a friend"""
        pass

class FriendSearchViewSet(viewsets.ViewSet):
    """
    friend search View Set
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendSearchSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def list(self, request):
        query = self.request.query_params.get('query', '')

        friendsId = list()
        friendsFriendsId = list()
        friends = Friend.objects.friends(request.user)

        for friend in friends:
            friendsId.append(friend.id)
            friends_of_friend = Friend.objects.friends(friend)

            for friend_friend in friends_of_friend:
                friendsFriendsId.append(friend_friend.id)

        queryset = (
            User.objects.filter(email__icontains=query) |
            User.objects.filter(first_name__icontains=query) |
            User.objects.filter(last_name__icontains=query)
        )

        friendsSet = queryset.filter(
            pk__in=friendsId
        ).exclude(
            pk=request.user.id
        ).distinct()

        friendsFriendsSet = queryset.filter(
            pk__in=friendsFriendsId
        ).exclude(
            pk__in=friendsId
        ).exclude(
            pk=request.user.id
        ).distinct()

        othersSet = queryset.exclude(
            pk__in=friendsId
        ).exclude(
            pk__in=friendsFriendsId
        ).exclude(
            pk=request.user.id
        ).distinct()

        serializer = self.serializer_class({
            'friends': friendsSet,
            'friends_friends': friendsFriendsSet,
            'others': othersSet,
        }, context={ 'request': request })

        return Response(serializer.data)
