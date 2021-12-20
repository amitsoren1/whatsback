from django.contrib import admin
from django.urls import path, include
from .views import LoginView, LogoutView, UserCreateAPIView, ProfileRetrieveUpdateAPIView, ContactListCreateAPIView

urlpatterns = [
    path('register', UserCreateAPIView.as_view(), name="create new user"),
    path('profile', ProfileRetrieveUpdateAPIView.as_view(), name="get profile of a user"),
    path('contact', ContactListCreateAPIView.as_view(), name="get or create contacts of a user"),
    path('login', LoginView.as_view(), name="Login user"),
    path('logout', LogoutView.as_view(), name="Logout user"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
