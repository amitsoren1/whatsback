from rest_framework import serializers

from users.models import User
from .models import Message, Chat
from datetime import datetime, timezone, timedelta
# from dateutil import relativedelta
import pytz
from django.conf import settings as conf_settings


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        ordering = ['date', 'time']
        read_only_fields = ["status", "sender"]
        # depth = 1

    def create(self, validated_data):
        # print(self.context.get("request"))
        return Message.objects.create(sender=self.context.get("profile"), **validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("chat", None)
        # representation.pop("sent_for", None)

        tz = pytz.timezone(conf_settings.TIME_ZONE)
        today = datetime.now(tz)
        yesterday = (today-timedelta(days=1))
        if today.date().strftime("%Y-%m-%d") == representation["date"]:
            representation["date"] = "TODAY"
        elif yesterday.date().strftime("%Y-%m-%d") == representation["date"]:
            representation["date"] = "YESTERDAY"
        return representation

    def validate(self, data):
        if self.context.get("profile") == data['sent_for']:
            raise serializers.ValidationError("Sender and receiver can't be same")
        return data

class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["time", "content", "sender", "sent_for", "date", "uid"]


class ChatCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="chat_with.owner.phone", read_only=True)

    # def get_chat_with(self, obj):
    #     return obj.chat_with

    class Meta:
        model = Chat
        ordering = ['id']
        exclude = ('owner',)
        # depth = 1
        read_only_fields = ["unread", "messages"]

    def create(self, validated_data):
        # print(self.context.get("request"))
        return Chat.objects.create(owner=self.context.get("profile"), **validated_data)


class ChatGetSerializer(serializers.ModelSerializer):
    messages = MessageCreateSerializer(many=True)
    phone = serializers.CharField(source="chat_with.owner.phone", read_only=True)

    class Meta:
        model = Chat
        # fields = "__all__"
        ordering = ['id']
        exclude = ('owner', )
        depth = 1
    # def to_representation(self, instance):
        # print(instance.messages.all())
        # representation = super().to_representation(instance)
        # representation["profile_picture"] = representation["chat_with"].pop("profile_picture", None)
        # representation["phone_number"] = representation["chat_with"].pop("phone_number", None)
        # representation["whatsapp_name"] = representation["chat_with"].pop("whatsapp_name", None)
        # representation["name"] = representation["chat_with"].pop("name", None)
        # representation["id"] = representation["chat_with"].pop("id", None)
        # representation.pop("chat_with")

        # representation.pop("owner")

        # return representation

class A(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"