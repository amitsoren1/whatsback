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
        return user


class ProfileSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="owner.phone", read_only=True)
    profile_picture = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        exclude = ("owner",)


class ContactCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField(max_length=10)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        read_only_fields = ('profile',)

    def validate_phone(self, phone):
        value = str(phone)
        if not value.isnumeric() or int(value)//1000000000 == 0:
            raise serializers.ValidationError(
                _(f"{value} is not a valid phone number"))
        contact_user = User.objects.filter(phone=phone).first()
        if contact_user is None:
            raise serializers.ValidationError("No user exists with this phone")
        return phone

    def create(self, validated_data):
        print(validated_data)
        contact_user = User.objects.filter(phone=validated_data.get("phone")).first()
        phone = validated_data.pop("phone")
        Contact.objects.create(owner=self.context.get("profile"), profile=contact_user.profile, **validated_data)
        return {**validated_data, "phone": phone, "profile": contact_user.profile}


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ("owner",)
        depth = 1


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
