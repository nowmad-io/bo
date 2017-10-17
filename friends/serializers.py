from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from .models import Friend, FriendshipRequest
from authentication.serializers import UserSerializer
import json

User = get_user_model()


class FriendshipRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    from_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    to_user = UserSerializer(read_only=True)
    to_user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user', 'from_user_id', 'to_user', 'to_user_id', 'message',
                  'created', 'rejected', 'viewed')

    def create(self, validated_data):
        """ create a friendship request """

        request = Friend.objects.add_friend(from_user=validated_data['from_user_id'],
                                            to_user=validated_data['to_user_id'],
                                            message=validated_data['message'])

        return request

class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend
        fields = ('from_user', 'to_user')
