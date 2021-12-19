from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, ProfileSerializer, ContactSerializer
import time


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self):
        return self.request.user.profile


class ContactListCreateAPIView(ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_queryset(self):
        return self.request.user.profile.contacts.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={
                                                'profile': request.user.profile
                                            }
                                        )
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
