from django.db.models.signals import post_save, post_delete
# from channels.db import database_sync_to_async
from django.dispatch import receiver
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Message, Chat
from .serializers import MessageCreateSerializer

@receiver(post_save, sender=Chat)
def create_chat(sender, instance, created, **kwargs):
    if created:
        Chat.objects.get_or_create(owner=instance.chat_with, chat_with=instance.owner)
        # chat1, exists = Chat.objects.get_or_create(owner=instance.sender,
        #     chat_with=instance.sent_for, uid="bf623dc0-df5d-4e61-809d-43ecf349a9d4")
        # chat1, exists = await database_sync_to_async(Chat.objects.get_or_create(owner=instance.sender, chat_with=instance.sent_for))
        # chat1.messages.add(instance)
        # chat1.save()

        # chat2, exists = Chat.objects.get_or_create(owner=instance.sent_for,
        #     chat_with=instance.sender, uid="bf623dc0-df5d-4e61-809d-43ecf349a9d4")
        # chat2, exists = await database_sync_to_async(Chat.objects.get_or_create(owner=instance.sent_for, chat_with=instance.sender))
        # chat2.unread += 1
        # chat2.messages.add(instance)
        # chat2.save()
        # serializer = MessageCreateSerializer(instance)
        # data = serializer.data
        # data["type"] = "incoming_message"
        # channel_layer = get_channel_layer()
        # # print(instance.sent_for.name)
        # async_to_sync(channel_layer.group_send)(
        #     f"chat_{str(instance.sent_for.id)}",
        #     data
        # )

@receiver(post_save, sender=Message)
def add_to_chat(sender, instance, created, **kwargs):
    if created:
        # Chat.objects.get_or_create(owner=instance.chat_with, chat_with=instance.owner)
        chat1 = Chat.objects.get(owner=instance.sender, chat_with=instance.sent_for)
        # chat1, exists = await database_sync_to_async(Chat.objects.get_or_create(owner=instance.sender, chat_with=instance.sent_for))
        chat1.messages.add(instance)
        chat1.save()

        chat2 = Chat.objects.get(owner=instance.sent_for, chat_with=instance.sender)
        # chat2, exists = await database_sync_to_async(Chat.objects.get_or_create(owner=instance.sent_for, chat_with=instance.sender))
        chat2.unread += 1
        chat2.messages.add(instance)
        chat2.save()

@receiver(post_delete, sender=Chat)
def update_messages(sender, instance, *args, **kwargs):
    if Chat.objects.filter(owner=instance.chat_with, chat_with=instance.owner).first() is None:
        for msg in Message.objects.filter(sender=instance.owner, sent_for=instance.chat_with) | Message.objects.filter(sender=instance.chat_with, sent_for=instance.owner):
            msg.delete()
