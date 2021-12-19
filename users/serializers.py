from rest_framework import serializers
from .models import User, Profile, Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        user = User.objects.create_user(validated_data.pop("email"), validated_data.pop("password"), **validated_data)
        Profile.objects.create(owner=user, name=user.username)
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
