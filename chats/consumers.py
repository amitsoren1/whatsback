# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat, Message
# from django.db.models import Q
# import random

# class ChatRoomConsumer(AsyncWebsocketConsumer):

#     def get_profile_id(self, user):
#         return str(user.profile.id)

#     def get_user_room_group_name(self, chat_id):
#         profile = Chat.objects.get(id=chat_id).chat_with
#         return f"chat_{str(profile.id)}"
    
#     def get_user_room_group_namebymsg(self, msg_id):
#         profile = Message.objects.get(id=msg_id).sender
#         return f"chat_{str(profile.id)}"

#     def get_self_profile_id(self):
#         return self.scope['user'].profile.id

#     def update_seen(self, chat_id):
#         chat = Chat.objects.get(id=chat_id)
#         chat.unread = 0
#         messages = chat.messages.all()
#         for msg in messages:
#             msg.status = "read"
#             msg.save()
#         chat.save()
    
#     def set_chat_as_read(self, chat_id):
#         chat = Chat.objects.get(id=chat_id)
#         chat.unread = 0
#         messages = chat.messages.all().filter(
#             (Q(status="sent") | Q(status="delivered")) & Q(sent_for=self.scope["user"].profile)
#         )
#         for msg in messages:
#             msg.status = "read"
#             msg.save()
#         chat.save()
    
#     def add_chat_with(self, text_data_json):
#         profile = Message.objects.get(id=text_data_json["message"]["id"]).sent_for
#         text_data_json["chat_with"] = {
#             "id": profile.id
#         }
    
#     def set_msg_as_delivered(self, msg_id):
#         msg = Message.objects.get(id=msg_id)
#         msg.status = "delivered"
#         msg.save()

#     async def connect(self):
#         user = self.scope['user']
#         if user.is_authenticated:
#             profile_id = await database_sync_to_async(self.get_profile_id)(user)
#             await self.accept()
#             self.room_group_name = f"chat_{profile_id}"
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#         else:
#             self.room_group_name = "notauthentictaed"

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
        
#         if text_data_json.get("type") == "messages_read":
#             await database_sync_to_async(self.set_chat_as_read)(text_data_json["chat_id"])
#             user_room_group_name = await database_sync_to_async(self.get_user_room_group_name)(text_data_json["chat_id"])
#             await self.channel_layer.group_send(
#                 user_room_group_name,
#                 {
#                     'type': 'messages_read',
#                     'chat_with': {
#                             "id": await database_sync_to_async(self.get_self_profile_id)()
#                                 }
#                 }
#             )
#         elif text_data_json.get("type") == "message_delivered":
#             await database_sync_to_async(self.set_msg_as_delivered)(text_data_json["message"]["id"])
#             user_room_group_name = await database_sync_to_async(self.get_user_room_group_namebymsg)(text_data_json["message"]["id"])
#             # await database_sync_to_async(self.add_chat_with)(text_data_json)
#             await self.channel_layer.group_send(
#                 user_room_group_name,
#                 {
#                     'type': 'message_delivered',
#                     'message': text_data_json["message"]
#                 }
#             )
#         else:
#             message = text_data_json['message']
#             username = text_data_json['username']

#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'chatroom_message',
#                     'message': message,
#                     'username': username,
#                 }
#             )

#     async def chatroom_message(self, event):
#         await self.send(text_data=json.dumps(event))
    
#     async def incoming_message(self, event):
#         await self.send(text_data=json.dumps(event))
    
#     async def messages_read(self, event):
#         # event["chat_with"] = {"id":}
#         await self.send(text_data=json.dumps(event))
    
#     async def message_delivered(self, event):
#         # event["chat_with"] = {"id":}
#         await self.send(text_data=json.dumps(event))

#     pass


# class VideoCallConsumer(AsyncWebsocketConsumer):
#     def get_profile_id(self, user):
#         return str(user.profile.id)

#     async def connect(self):
#         user = self.scope['user']
#         if user.is_authenticated:
#             profile_id = await database_sync_to_async(self.get_profile_id)(user)
#             # print(profile_id)
#             await self.accept()
#             self.room_group_name = f"call_{profile_id}"
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name
#             )
#         # n = random.randint(10,22222)
        
#         # self.room_group_name = str(n)
#         # await self.channel_layer.group_add(
#         #     self.room_group_name,
#         #     self.channel_name
#         # )
#         # await self.accept()
#         # print(list(self.channel_layer.groups.keys()))

#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                     {
#                         'type': 'yourID',
#                         'id': self.room_group_name
#                     }
#                     )
#         else:
#             self.room_group_name = "unauthenticated"
#             print("UNAUTHENTICATED SOCKET")

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         # print(text_data_json)
#         if text_data_json["type"] == "callUser":
#             profile_id = text_data_json["to"]
#             await self.channel_layer.group_send(
#                 f"call_{profile_id}",
#                 # list(self.channel_layer.groups.keys())[2],
#                 {
#                     'type': 'hey',
#                     'signalData': text_data_json["signalData"],
#                     'from': text_data_json["from"],
#                     # 'to': text_data_json["to"]
#                 }
#                 )
        
#         if text_data_json["type"] == "acceptCall":
#             # print(text_data_json["to"])
#             profile_id = text_data_json["to"]["id"]
#             await self.channel_layer.group_send(
#                 f"call_{profile_id}",
#                 # list(self.channel_layer.groups.keys())[1],
#                 {
#                     'type': 'callAccepted',
#                     'signalData': text_data_json["signal"],
#                     # 'from': text_data_json["from"],
#                     # 'to': text_data_json["to"]
#                 }
#                 )
        
#         if text_data_json["type"] == "disconnect_call":
#             # print(text_data_json)
#             profile_id = text_data_json["to"]["id"]
#             await self.channel_layer.group_send(
#                 f"call_{profile_id}",
#                 # list(self.channel_layer.groups.keys())[1],
#                 {
#                     'type': 'disconnect_call',
#                 }
#                 )

#     async def chatroom_message(self, event):
#         await self.send(text_data=json.dumps(event))

#     async def hey(self, event):
#         await self.send(text_data=json.dumps(event))
    
#     async def yourID(self, event):
#         await self.send(text_data=json.dumps(event))
    
#     async def callAccepted(self, event):
#         await self.send(text_data=json.dumps(event))
    
#     async def disconnect_call(self, event):
#         await self.send(text_data=json.dumps(event))