from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("chat", consumers.ChatRoomConsumer.as_asgi()),
    path("video", consumers.VideoCallConsumer.as_asgi()),
]
