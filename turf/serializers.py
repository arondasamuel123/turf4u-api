from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from turfapi.models import Turf, Organization


class OrgSerializer(serializers.ModelSerializer):
    """
    Serializer class for Organization Model
    """
    org_created = serializers.DateTimeField(default=timezone.now, required=False)
    user = serializers.ReadOnlyField(source='user.id')
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
    org = serializers.ReadOnlyField(source='org.id')

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


class UpdateImageUrlSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField()

    class Meta:
        model = Turf
        fields = ['id', 'image_url']
