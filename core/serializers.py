from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from core.models import Review, Location

User = get_user_model()

# Serializers define the API representation.
# class UserSerializer(serializers.Serializer):
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#
#     def create(self, *args, **kwargs):
#         return  User().save(*args, **kwargs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')
        depth = 1

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('longitude', 'latitude')

class ReviewSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False,)

    class Meta:
        model = Review
        fields = ('id', 'title', 'description', 'privacy', 'location')

    def create(self, validated_data):
        #validated_data contains all data from the serializer

        #set up created_by attribute with logged user or None
        user = None
        request = self.context['request']
        if request and hasattr(request, "user"):
            user = request.user
            validated_data['created_by'] = user

        # create location manually (DRF doesn't handle nested creation or update)
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        validated_data['location'] = location

        review = Review.objects.create(**validated_data)

        return review

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.privacy = validated_data.get('privacy', instance.privacy)

        # handle manually location
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        instance.location = location

        instance.save()
        return instance
