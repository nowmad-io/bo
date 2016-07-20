from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from serializers import UserSerializer, ReviewSerializer
from rest_framework.decorators import list_route
from models import Review

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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

# class UserViewSet(viewsets.ViewSet):
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = UserSerializer
#
#     def add_friends(self, request):
#         pass
#
#     def rmv_friends(self, request):
#         pass

class ReviewViewSet(viewsets.ViewSet):
    """
    Review View Set
    """
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReviewSerializer

    def list(self, request):
        if request.user.is_authenticated():
            queryset = Review.objects.filter(created_by = request.user)
        else:
            queryset = Review.objects.all()

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data = request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED
            )

        return Response({
            'status': 'Bad request',
            'message': 'Review could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        myreview = get_object_or_404(queryset, pk = pk)

        serializer = ReviewSerializer(myreview)
        return Response(serializer.data)


    def update(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'Review could not be find.'
            }, status=HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(review, data = request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.validated_data, status=status.HTTP_202_ACCEPTED
            )

        return Response({
            'status': 'Bad request',
            'message': 'Review could not be updated with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
