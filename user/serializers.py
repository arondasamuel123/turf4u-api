from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from turfapi.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class for Custom User Model
    """

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'is_manager']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        """
        Create user with custom User Model
        """
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class QueryTokenSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=1)


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer to obtain token using email
    """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")

        attrs['user'] = user
        return attrs
