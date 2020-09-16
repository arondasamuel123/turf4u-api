from django.core import signing
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status


from .serializers import UserSerializer, AuthTokenSerializer, \
    QueryTokenSerializer
from turfapi.models import User
from .confirm_email import send_confirmation_email


class RegisterUser(generics.CreateAPIView):
    """
    API view to create/register user
    """
    def post(self, request, format=None):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['is_active'] = False
            serializer.save()

            user = User.objects.filter(email=serializer.data['email']).first()
            send_confirmation_email(
                user.email, user.generate_confirmation_token()
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountActivationView(generics.CreateAPIView):
    """
    API View to activate a user's account based on the validity of
    token sent to user's email address
    """
    def post(self, request, format=None):
        serializer = QueryTokenSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        try:
            token_data = signing.loads(
                serializer.data['token'], max_age=13800
            )
        except Exception:
            return Response(
                {
                    'message': 'Invalid token provided'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=token_data['user_email']).first()
        if user is None:
            return Response(
                {
                    'message': 'Invalid token provided'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if user.is_active:
            return Response(
                {
                    'message': f'Account of {user.email} already activated'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = True
        user.save()
        return Response(
            {
                'message': f'Account of {user.email} activated'
            },
            status=status.HTTP_200_OK
        )


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
