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

class ReviewViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        queryset = Review.objects.all()

        # print queryset.keys
        # queryset = Review.objects.filter(created_by = request.user)
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    # @list_route(
    #     methods=['post'],
    #     permission_classes=(IsAuthenticated,),
    #     # serializer_class=CustomPostSerializer,
    #     # pagination_class=LimitOffsetPagination,
    #     url_path='create',
    # )
    def create(self, request):
        print request.body
        serializer = ReviewSerializer(data = request.body)
        if serializer.is_valid():
            print 'valid'
            serializer.save()
        return Response(serializer.data)

    # def perform_create(self, serializer):
    #     print 'blabla'
    #     print self.request.user.get_full_name()
    #     serializer.save()


    def retrieve(self, request, pk=None):
        queryset = Review.objects.all()
        myreview = get_object_or_404(queryset, pk = pk)

        serializer = ReviewSerializer(myreview)
        return Response(serializer.data)


    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

# class ReviewViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.AllowAny,)
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def perform_create(self, serializer):
#         print 'blabla'
#         print self.request.user.get_full_name()
#         serializer.save()
