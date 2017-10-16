from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from core.serializers import ReviewSerializer, UserSerializer

class ReviewDetailsSerializer(ReviewSerializer):
    created_by = UserSerializer(many=False,)

    class Meta(ReviewSerializer.Meta):
        fields = ('id', 'title', 'description', 'location', 'created_by', 'categories')
