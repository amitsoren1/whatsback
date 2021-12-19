from rest_framework.generics import (
                                     ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                     ListAPIView, RetrieveAPIView
                                )
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Message, Chat
from .serializers import MessageCreateSerializer, A, MessageUpdateSerializer, ChatSerializer
import time
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import Http404

class MessageListCreateAPIView(ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     "chat_chat",
        #     {
        #         'type': 'chatroom_message',
        #         'message': "message",
        #         'username': "username123",
        #     }
        # )
        return Message.objects.filter(
                Q(sender=self.request.user.profile) | Q(sent_for=self.request.user.profile)
                )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={
                                                'profile': request.user.profile
                                            }
                                        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MessageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageUpdateSerializer
    # lookup_field = "uid"

class ChatListAPIView(ListAPIView):
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # time.sleep(10)
        # messages = Message.objects.filter(sent_for=self.request.user.profile)
        return self.request.user.profile.chats.all().order_by("-updated_on")

# from django.shortcuts import render


# def room(request, room_name):
#     return render(request, 'chatroom.html', {
#         'room_name': room_name
#     })

class ChatwithRetrieveAPIView(RetrieveAPIView):
    serializer_class = ChatSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Chat.objects.filter(owner=self.request.user.profile,
                                   chat_with__id=self.kwargs[self.lookup_field]).first()
        if obj:
            self.check_object_permissions(self.request, obj)
            return obj
        raise Http404


class ChatRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
