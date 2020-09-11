from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from turfapi.models import Turf, Organization, User
# from user.serializers import UserSerializer


class OrgSerializer(serializers.ModelSerializer):
    """
    Serializer class for Organization Model
    """
    org_created = serializers.DateTimeField(default=timezone.now, required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    organization_email = serializers.EmailField(required=False)

    class Meta:
        model = Organization
        fields = [
            'id',
            'organization_email',
            'organization_name',
            'organization_location',
            'contact_number',
            'user',
            'org_created'
        ]
        read_only_field = ['id', ]
        validators = [
            UniqueTogetherValidator(
                fields=['contact_number', 'organization_name'],
                queryset=Organization.objects.all(),
                message="Organization already exists"
            )
        ]


class TurfSerializer(serializers.ModelSerializer):
    """
    Serializer class for Turf Model
    """
    turf_created = serializers.DateTimeField(default=timezone.now, required=False)
    turf_image = serializers.CharField(required=False)
    org = OrgSerializer(read_only=True)

    class Meta:
        model = Turf
        fields = ['id', 'turf_name', 'no_of_pitches', 'turf_image', 'org', 'turf_created']
        read_only_field = ['org', 'id', ]
        validators = [
            UniqueTogetherValidator(
                fields=['turf_name', 'turf_created'],
                queryset=Turf.objects.all(),
                message="Turf already exists"
            )
        ]
