from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework import generics

from django.shortcuts import render
from .serializers import FriendSerializer, FriendshipRequestSerializer, FriendshipIdSerializer
from core.serializers import UserSerializer
from .models import Friend

# Create your views here.

class FriendshipRequestViewSet(viewsets.ViewSet):
    """
        standard behaviour for friendship request
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipRequestSerializer

    def list(self, request):
        """ return the list of friendship request """
        print "in standard"
        pass

    def retrieve(self, request, pk):
        """ get info from the friendhsip request with pk = pk"""
        pass

    def destroy(self, request, pk):
        """ delete friendship request with pk=pk """
        pass

    def create(self, request):
        """ create a friendship request """

        #chek if there is a from_user
        if 'from_user' not in request.data:
            # raise error
            pass


        #check the user performing the request is the user authenticated
        if request.data['from_user'] != request.user.id:
            return Response({'status':'WhoAreYou ??'},  status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

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
        queryset = Friend.objects.requests(user = request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def outgoing_list(self, request):
        """List friends request of authenticated user"""
        queryset = Friend.objects.sent_requests(user = request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FriendshipEventViewset(viewsets.ViewSet):
    """
        manage incoming friendship request
        print the list of incoming friendship request
        validate incoming friendship request
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendshipIdSerializer

    def accept(self, request, pk):
        """ accept a request """
        """ validate a friendship request """

        #chek if there is a from_user
        if 'to_user' not in request.data:
            # raise error
            pass

        #check the user performing the request is the user authenticated
        if request.data['to_user'] != request.user.id:
            return Response({'status':'WhoAreYou ??'},  status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        print request.data['id']

        #get the data back
        serializer = self.serializer_class(
            data = request.data,
            context={'to_user': request.user.id})
        print "WHHHHHAAATT"
        print serializer.initial_data
        #build the request in the backend
        if serializer.is_valid():
            print serializer.data
            serializer.accept(serializer.data)
            return Response(status = status.HTTP_201_CREATED)

        return Response({
              'status': 'Bad request',
              'message': serializer.errors,
              'value': serializer.initial_data
          }, status=status.HTTP_400_BAD_REQUEST)


    def reject(self, request, pk):
        """ reject a friendship request """





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

    # def create(self, request):
    #     """ cannot create friends directly, need to pass by a request """
    #     pass
