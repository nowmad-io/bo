from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets

User = get_user_model()

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'email', 'password')
