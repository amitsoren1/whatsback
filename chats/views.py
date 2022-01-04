import json
from datetime import date
import threading
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import QueryDict
from rest_framework.generics import (
                                     CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                     ListAPIView, RetrieveAPIView
                                )
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.views import APIView

from users.models import Profile
from .models import Message, Chat
from .serializers import (MessageCreateSerializer, A, MessageUpdateSerializer,
                            ChatCreateSerializer, ChatGetSerializer)
import time
# from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import Http404

def new_message(message):
    Message.objects.create(uid=message["newMsgObject"]["uid"], content=message["newMsgObject"]["content"],
        sender=Profile.objects.get(id=message["newMsgObject"]["sender"]["id"]),
        sent_for=Profile.objects.get(id=message["newMsgObject"]["sent_for"]),
        time=message["newMsgObject"]["time"], date=message["newMsgObject"]["date"])

def update_read_messages(reader_id, chat_with_id):
    chat = Chat.objects.get(owner=chat_with_id, chat_with=reader_id)
    for message in chat.messages.filter(sender__id=chat_with_id):
        message.status = Message.STATUS[2][0]
        message.save()
    mychat = Chat.objects.get(owner=reader_id, chat_with=chat_with_id)
    mychat.unread=0
    mychat.save()

@require_http_methods(["PATCH"])
@csrf_exempt
def new_message_view(request):
    data_str = request.body.decode()
    data = json.loads(data_str)

    T = threading.Thread(target=new_message, args=(data,))
    T.start()
    return JsonResponse({"result": "worked"})

@require_http_methods(["PATCH"])
@csrf_exempt
def update_read_view(request):
    data_str = request.body.decode()
    data = json.loads(data_str)

    T = threading.Thread(target=update_read_messages, args=(data["reader"], data["chat_with"]))
    T.start()
    return JsonResponse({"result": "worked"})

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
    serializer_class = ChatGetSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.chats.all().order_by("-updated_on")


class ChatCreateAPIView(CreateAPIView):
    serializer_class = ChatCreateSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

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

# from django.shortcuts import render


# def room(request, room_name):
#     return render(request, 'chatroom.html', {
#         'room_name': room_name
#     })

class ChatwithRetrieveAPIView(RetrieveAPIView):
    serializer_class = ChatGetSerializer
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
    serializer_class = ChatGetSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = Chat.objects.filter(owner=self.request.user.profile,
                                  id=self.kwargs[self.lookup_field]).first()
        if obj:
            self.check_object_permissions(self.request, obj)
            return obj
        raise Http404


class Aview(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    # def get(self, request):
    #     with open("asd.txt", "r") as f:
    #         q=f.readlines()
    #     return JsonResponse({"res": q})
    def get(self, request):
        obj = Message(sender=request.user.profile, sent_for=request.user.profile,
                      content="hello", uid="bf623dc0-df5d-4e61-809d-43ecf349a9d4",
                      time="2:20", date="2021-12/10")
        obj.save()
        return JsonResponse({"res": obj.__dict__})
