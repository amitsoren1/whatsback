from django.contrib import admin
from django.urls import path, include
from .views import UserCreateAPIView, ProfileRetrieveUpdateAPIView, ContactListCreateAPIView

urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name="create new user"),
    path('profile', ProfileRetrieveUpdateAPIView.as_view(), name="get profile of a user"),
    path('contact', ContactListCreateAPIView.as_view(), name="get or create contacts of a user"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
