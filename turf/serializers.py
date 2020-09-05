from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from turfapi.models import Turf, Organization


class TurfSerializer(serializers.ModelSerializer):
    """
    Serializer class for Turf Model
    """
    turf_created = serializers.DateTimeField(default=timezone.now, required=False)

    class Meta:
        model = Turf
        fields = ['turf_name', 'turf_location', 'turf_image', 'org', 'turf_created']
        read_only_field = ['org']
        validators = [
            UniqueTogetherValidator(
                fields=['turf_name', 'turf_location'],
                queryset=Turf.objects.all(),
                message="Turf already exists"
            )
        ]


class OrgSerializer(serializers.ModelSerializer):
    """
    Serializer class for Organization Model
    """
    org_created = serializers.DateTimeField(default=timezone.now, required=False)

    class Meta:
        model = Organization
        fields = [
            'organization_email',
            'organization_name',
            'contact_number',
            'user',
            'org_created'
        ]
        read_only_field = ['user']
        validators = [
            UniqueTogetherValidator(
                fields=['organization_email', 'organization_name'],
                queryset=Organization.objects.all(),
                message="Organization already exists"
            )
        ]
