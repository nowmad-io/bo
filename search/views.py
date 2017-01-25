from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from core.serializers import ReviewSerializer
from core.models import Review
from friends.models import Friend
from search.serializers import ReviewDetailsSerializer

# Create your views here.
class SearchReviews(generics.ListAPIView):
    serializer_class = ReviewDetailsSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """

        friends = Friend.objects.friends(self.request.user)
        friends.append(self.request.user)

        queryset = Review.objects.filter(created_by__in=friends)

        # friends = self.request.query_params.get('friends', None)
        #
        return queryset
