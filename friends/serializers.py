from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from .models import Friend, FriendshipRequest


User = get_user_model()

class FriendshipRequest(serializers.ModelSerializer):

    class Meta:
        model = FriendshipRequest
        fields = ('from_user', 'to_user', 'message', 'created', 'rejected', 'viewed')


class FriendSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friend
        fields = ('from_user', 'to_user')

    def create(self, validated_data):

        #validated_data contains all data from the serializer
        return Friend.objects.add_friend(**validated_data)

        # #set up created_by attribute with logged user or None
        # from_user = None
        # to_user = None
        # request = self.context['request']
        #
        # if request and hasattr(request, "from_user"):
        #     user = request.from_user
        #     validated_data['created_by'] = user
        #
        # # create location manually (DRF doesn't handle nested creation or update)
        # location_data = validated_data.pop('location')
        # location, _ = Location.objects.get_or_create(**location_data)
        # validated_data['location'] = location
        #
        # review = Review.objects.create(**validated_data)
        #
        # return review

    def update(self, instance, validated_data):
        pass
