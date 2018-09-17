from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Count, Q
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from itertools import chain
from rest_framework.decorators import list_route
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions, viewsets
from rest_framework import generics

from .serializers import ReviewSerializer, ReviewsSerializer, CategorySerializer, PlacesSerializer, PlacesSearchSerializer, ReviewPicturesSerializer
from .models import Place, Review, Category, InterestedPeople
from friends.models import Friend

User = get_user_model()

class PlaceListView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PlacesSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        query = self.request.query_params.get('query', '')
        email = self.request.query_params.get('user', '')

        if query or email:
            return PlacesSearchSerializer
        else:
            return PlacesSerializer

    def get_queryset(self):
        """
        Get places where a friends put a review
        """
        query = self.request.query_params.get('query', '')
        email = self.request.query_params.get('user', '')

        if email:
            all_friends = list([User.objects.get(email=email)])
        else:
            friends = Friend.objects.friends(self.request.user)
            all_friends = list(friends)

            for friend in friends:
                friend_friends = Friend.objects.friends(friend)
                all_friends = list(chain(all_friends, friend_friends))

            all_friends.append(self.request.user)

        pre_queryset = Review.objects.filter(Q(created_by__in=all_friends) | Q(public=True))

        if query:
            pre_queryset = pre_queryset.filter(Q(short_description__icontains=query) | Q(information__icontains=query))

        queryset = Place.objects.filter(
            reviews__in=pre_queryset
        ).prefetch_related(Prefetch(
            'reviews',
            queryset=pre_queryset,
        )).distinct()

        return queryset

class CategoryViewSet(viewsets.ViewSet):
    """
        Category View Set
    """

    #Manage the permission to the view set, only when authenticated
    permission_classes = (permissions.IsAuthenticated,)
    # two kind of authentication, token to be easier for test
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = CategorySerializer

    def list (self, request):
        queryset = Category.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class ReviewViewSet(viewsets.ViewSet):
    """
    Review View Set
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = ReviewSerializer

    def list(self, request):
        if request.user.is_authenticated:
            queryset = Review.objects.filter(created_by = request.user)
        else:
            queryset = Review.objects.all()

        serializer = self.serializer_class(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data = request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )

        return Response({
            'status': 'Bad request',
            'message': 'Review could not be created with received data.',
            'data': str(request.data),
            'validated_data': serializer.validated_data,
            'errors': serializer.errors
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
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(review, data = request.data, context={'request':request})
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

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk, created_by=request.user)
            review.delete()
        except Review.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'Bookmark could not be find.'
            }, status=HTTP_404_NOT_FOUND)

        return Response({
            'status': 'Success',
            'message': 'Bookmark deleted'
        }, status=status.HTTP_200_OK)

class ReviewPicturesViewSet(viewsets.ViewSet):
    """
    Update Review's Pictures
    """
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = ReviewPicturesSerializer

    def update(self, request, pk=None):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({
                'status': 'Not Found',
                'message': 'Review could not be find.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(review, data = request.data, context={'request':request})

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
