from django.contrib import admin
from django.urls import path, include
from .views import (MessageListCreateAPIView, MessageRetrieveUpdateDestroyAPIView,
                    ChatListAPIView, ChatwithRetrieveAPIView, ChatRetrieveUpdateDestroyAPIView
                )

urlpatterns = [
    path('message', MessageListCreateAPIView.as_view(), name="create or list messages"),
    path('message/<int:pk>', MessageRetrieveUpdateDestroyAPIView.as_view(), name="get or update a message"),
    path("chat", ChatListAPIView.as_view(), name="chats of authenticated user"),
    path('chat-with/<int:pk>', ChatwithRetrieveAPIView.as_view(), name="get a chat of user with user pk"),
    path('chat/<int:pk>', ChatRetrieveUpdateDestroyAPIView.as_view(), name="get a chat with id pk"),
]


# from . import views

# urlpatterns = [
#     path('<str:room_name>/', views.room, name='room'),
# ]