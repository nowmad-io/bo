from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField

from itertools import chain
from rest_framework import serializers, viewsets

from core.models import Review, Place, Category, Picture
from friends.models import Friend
from authentication.serializers import UserSerializer

User = get_user_model()

def getUserType(self, obj):
    currentUser = self.context['request'].user
    friends = Friend.objects.friends(currentUser)
    friends_friends = list()

    for friend in friends:
        friend_friends = Friend.objects.friends(friend, [currentUser])
        friends_friends = list(chain(friends_friends, friend_friends))

    if (obj.created_by == currentUser):
        return 'me'

    if (obj.created_by in friends):
        return 'friend'

    if (obj.created_by in friends_friends):
        return 'friends_friend'

    return ''

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.CharField()

    class Meta:
        model = Place
        fields = ('id', 'place_id', 'name', 'longitude', 'latitude', 'address')

class PictureSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    uri = serializers.CharField(required=False)
    caption = serializers.CharField(allow_blank=True)

    class Meta:
        model = Picture
        fields = ('id', 'uri', 'caption')

class ReviewsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    pictures = PictureSerializer(required=False, many=True)
    created_by = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'place', 'short_description', 'information', 'categories', 'pictures', 'status', 'created_by', 'user_type', 'creation_date', 'link_1', 'link_2')

    def get_user_type(self, obj):
        return getUserType(self, obj)

class ReviewSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(many=False)
    categories = CategorySerializer(many=True)
    pictures = PictureSerializer(required=False, many=True, read_only=True)
    created_by = UserSerializer(default=serializers.CurrentUserDefault(), read_only=True)
    user_type = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'short_description', 'information', 'place', 'categories', 'pictures', 'status', 'created_by', 'user_type', 'creation_date', 'public', 'link_1', 'link_2')

    def create(self, validated_data):
        category_list=[]

        # create place manually (DRF doesn't handle nested creation or update)
        place_data = validated_data.pop('place')
        place, _ = Place.objects.get_or_create(**place_data)
        validated_data['place'] = place

        # remove the categories properties
        if 'categories' in validated_data:
            category_list = validated_data.pop('categories')

        # remove the pictures properties
        if 'pictures' in validated_data:
            pictures_list = validated_data.pop('pictures')

        #we create the review object
        review = Review.objects.create(**validated_data)

        #we add the category, one by one
        for category in category_list:
            getCategory = Category.objects.get(name=category['name'])
            review.categories.add(getCategory)

        for picture in pictures_list:
            newPicture = Picture.objects.create(**picture)
            review.pictures.add(newPicture)

        return review

    def update(self, instance, validated_data):
        instance.short_description = validated_data.get('short_description', instance.short_description)
        instance.information = validated_data.get('information', instance.information)
        instance.status = validated_data.get('status', instance.status)

        newCategories = []
        categories = validated_data.get('categories', instance.categories)
        for category in categories:
            newCategories.append(Category.objects.get(name=category['name']))

        instance.categories.set(newCategories)

        instance.save()
        return instance

    def get_user_type(self, obj):
        return getUserType(self, obj)

class ReviewPicturesSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)

    class Meta:
        model = Review
        fields = ('id', 'pictures',)

    def update(self, instance, validated_data):
        newPictures = []
        pictures = validated_data.get('pictures', instance.pictures)
        print('yooo pictures', pictures)
        for picture in pictures:
            pic, _ = Picture.objects.get_or_create(**picture)
            print('pic', pic)
            newPictures.append(pic)
        print('new pictures', newPictures)
        instance.pictures.set(newPictures)

        instance.save()
        return instance

class PlacesSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'place_id', 'name', 'longitude', 'latitude', 'address', 'reviews')

class PlacesSearchSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    all_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ('id', 'place_id', 'name', 'longitude', 'latitude', 'address', 'reviews', 'all_reviews')

    def get_reviews(self, obj):
        queryset = obj.reviews
        email = self.context['request'].query_params.get('user', '')
        if email:
            user = User.objects.get(email=email)
            queryset = queryset.filter(created_by = user)

        return ReviewsSerializer(queryset, many=True, context=self.context).data

    def get_all_reviews(self, obj):
        return ReviewsSerializer(obj.reviews, many=True, context=self.context).data
