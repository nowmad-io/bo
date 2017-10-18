from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets

from core.serializers import ReviewSerializer
from authentication.serializers import UserSerializer

class ReviewDetailsSerializer(ReviewSerializer):
    created_by = UserSerializer(many=False,)

    class Meta(ReviewSerializer.Meta):
        fields = ('id', 'title', 'description', 'place', 'created_by', 'categories')
