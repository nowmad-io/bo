from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from .models import Friend, FriendshipRequest
from core.serializers import UserSerializer
import json


User = get_user_model()

class FriendshipIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = ('id',)

    def accept(self, validated_data):
        """ accept a friendship request from the id provided """
        print(json.dumps(validated_data, indent=4))
        print validated_data.keys
        print validated_data['id']

        #get the record with id = validated_data['id']
        request = FriendshipRequest.get_object_or_404(id=validated_data['id'])
        # accpet the friendship request
        result = request.accept()
        return result

class FriendshipRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'from_user', 'to_user', 'message', 'created', 'rejected', 'viewed')

    def create(self, validated_data):
        """ create a friendship request """

        request = Friend.objects.add_friend(from_user=validated_data['from_user'],
                                            to_user=validated_data['to_user'],
                                            message=validated_data['message'])

        return request


    def validate(self, validated_data):
        """ validate a friend request """
        print 'IN MOTHER FUCKER'

        request = FriendshipRequest.get_object_or_404(from_user = validated_data['from_user'],
                                                      to_user = validated_data['to_user'] )


        request.accept()

        return request


class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend
        fields = ('from_user', 'to_user')
