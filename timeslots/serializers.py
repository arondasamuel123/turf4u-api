from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from turfapi.models import Timeslots, Booking
from user.serializers import UserSerializer


class ListTimeslotsSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        result = [Timeslots(**attrs) for attrs in validated_data]
        return Timeslots.objects.bulk_create(result)


class TimeslotsSerializer(serializers.ModelSerializer):
    turf = serializers.ReadOnlyField(source='turf.id')

    class Meta:
        model = Timeslots
        fields = ['id', 'start_time', 'stop_time', 'turf', 'price']
        list_serializer_class = ListTimeslotsSerializer


class BookingsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    timeslot = TimeslotsSerializer(read_only=True)
    date_booked = serializers.DateField(
        validators=[UniqueValidator(
            queryset=Booking.objects.all(),
            message="The timeslot has already been booked"
        )])

    class Meta:
        model = Booking
        fields = [
            'id',
            'user',
            'timeslot',
            'date_booked',
            'payment_method',
            'payment_status'
        ]
