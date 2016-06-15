from django.conf.urls import url, include
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from core.models import Review

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
        fields = ('id', 'first_name', 'last_name', 'email', 'location')
        depth = 1

# class GetToken(APIView):
#     throttle_classes = ()
#     permission_classes = (AllowAny,)
#     authentication_classes = (TokenAuthentication,)
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
#     renderer_classes = (renderers.JSONRenderer,)
#     def post(self, request):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})

class ReviewSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    privacy = serializers.IntegerField()
    location_id = serializers.IntegerField()
    # created_by = serializers.IntegerField()

    def create(self, validated_data):
        #validated_data contains all data from the serializer
        #after the JSONParser so that we have a dict
        #we need to get the right
        user = None
        request = self.context['request']
        print request
        if request and hasattr(request, "user"):
            user = request.user
        validated_data['created_by'] = user
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.privacy = validated_data.get('privacy', instance.privacy)
        instance.save()
        return instance

# class ReviewSerializer(serializers.ModelSerializer):
#     created_by = serializers.PrimaryKeyRelatedField(read_only=True)
#
#     class Meta:
#         model = Review
#         fields = ('id', 'title', 'description', 'location', 'privacy', 'category', 'created_by', 'creation_date')
#         depth = 2
