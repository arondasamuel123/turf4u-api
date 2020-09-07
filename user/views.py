from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from .serializers import UserSerializer, AuthTokenSerializer


class RegisterUser(generics.CreateAPIView):
    """
    API view to create/register user
    """
    serializer_class = UserSerializer


class CustomObtainToken(ObtainAuthToken):
    """
    Custom API view to generate new token
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RetrieveUpdateUser(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update user
    """
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        """
        Retrieve authenticated user
        """
        return self.request.user
