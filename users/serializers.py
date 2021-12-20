from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token
from .models import User, Profile, Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data.pop("phone"), validated_data.pop("password"), **validated_data)
        Profile.objects.create(owner=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ("owner",)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ("owner",)
        depth = 1
    
    def create(self, validated_data):
        # print(self.context.get("request"))
        if User.objects.filter(email=validated_data.get("email")).first() is None:
            raise serializers.ValidationError("No user exists with this email")
        return Contact.objects.create(owner=self.context.get("profile"), **validated_data)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_phone(self, phone, password):
        user = None

        if phone and password:
            user = self.authenticate(phone=phone, password=password)
        else:
            msg = _('Must include "phone" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        user = None

        if phone:
            user = self._validate_phone(phone, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for Token model.
    """

    class Meta:
        model = Token
        fields = ('key',)
