from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from djoser import constants, utils

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    public_default = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'picture', 'public_default')

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()

        return instance

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'picture', 'email', 'password')

    def validate_email(self, email):
        return email.lower()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class TokenCreateSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )

    default_error_messages = {
        'invalid_credentials': constants.INVALID_CREDENTIALS_ERROR,
        'inactive_account': constants.INACTIVE_ACCOUNT_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super(TokenCreateSerializer, self).__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(
            required=False
        )

    def validate(self, attrs):
        self.user = authenticate(
            username=attrs.get(User.USERNAME_FIELD).lower(),
            password=attrs.get('password')
        )

        self._validate_user_exists(self.user)
        self._validate_user_is_active(self.user)
        return attrs

    def _validate_user_exists(self, user):
        if not user:
            self.fail('invalid_credentials')

    def _validate_user_is_active(self, user):
        if not user.is_active:
            self.fail('inactive_account')
