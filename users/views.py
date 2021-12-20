from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from django.conf import settings

from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import LoginSerializer, TokenSerializer, UserSerializer, ProfileSerializer, ContactSerializer
import time

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password'
    )
)

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


class LoginView(GenericAPIView):
    """
    Check the credentials and return the REST Token
    if the credentials are valid and authenticated.
    Calls Django Auth login method to register User ID
    in Django session framework
    Accept the following POST parameters: phone, password
    Return the REST Framework Token Object's key.
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    token_model = Token

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token, _ = Token.objects.get_or_create(user=self.user)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_login(self.request, self.user)

    def get_response(self):
        serializer = TokenSerializer(instance=self.token,
                                     context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = self.http_method_not_allowed(request, *args, **kwargs)

        return self.finalize_response(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": _("Successfully logged out.")},
                            status=status.HTTP_200_OK)
        return response
