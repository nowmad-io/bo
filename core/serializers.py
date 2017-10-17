from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets

from core.models import Review, Location, Category
from authentication.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'icon')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('longitude', 'latitude')

class ReviewSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=False,)
    categories = CategorySerializer(many=True)
    created_by = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'title', 'description', 'location', 'categories', 'created_by')

    def create(self, validated_data):
        category_list=[]

        # create location manually (DRF doesn't handle nested creation or update)
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        validated_data['location'] = location

        #we remove the category properties
        if 'categories' in validated_data:
            category_list = validated_data.pop('categories')

        #we create the review object
        review = Review.objects.create(**validated_data)

        #we add the category, one by one
        for category in category_list:
            newCategory, created = Category.objects.get_or_create(name=category['name'])

            if 'icon' in category and category['icon'] is not None:
                newCategory.icon = category['icon']
                newCategory.save()

            review.categories.add(newCategory)

        return review

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        # handle manually location
        location_data = validated_data.pop('location')
        location, _ = Location.objects.get_or_create(**location_data)
        instance.location = location

        instance.save()
        return instance
