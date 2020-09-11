from rest_framework import serializers

from turfapi.models import Timeslots


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
