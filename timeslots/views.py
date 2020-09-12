from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from turfapi.models import Turf, Timeslots, Booking
from .serializers import TimeslotsSerializer,\
    BookingsSerializer
from .permissions import IsTurfManager


class ListCreateTimeslots(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # def get_queryset(self, pk):
    #     turf = Turf.objects.get(pk=pk)
    #     return Timeslots.objects.filter(turf_id=turf.id)

    def post(self, request, pk):
        turf = Turf.objects.get(pk=pk)
        is_many = isinstance(request.data, list)
        if is_many:
            serializer = TimeslotsSerializer(
                data=request.data,
                many=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(turf=turf)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            serializer = TimeslotsSerializer(
                data=request.data,
                many=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(turf=turf)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateTimeslot(generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = TimeslotsSerializer
    queryset = Timeslots.objects.all()


class RetrieveTimeslotByTurf(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        timeslots = Timeslots.objects.filter(
            turf_id=kwargs['pk']
        ).all()
        serializer = TimeslotsSerializer(
            timeslots,
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class MakeBooking(generics.CreateAPIView):
    """
    API View that users will use to make a
    booking
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        timeslot = Timeslots.objects.get(
            pk=kwargs['pk']
        )
        bookings = Booking.objects.filter(
            user=request.user
        ).all()
        serializer = BookingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for booking in bookings:
            if booking.payment_status == 'not_paid':
                return Response(
                    "Please complete payment for last booking made",
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer.save(timeslot=timeslot, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReadUpdateDeleteBooking(generics.RetrieveUpdateDestroyAPIView):
    """
    API View to retrieve, update and delete a booking for a specific
    timeslot
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsTurfManager]
    queryset = Booking.objects.all()
    serializer_class = BookingsSerializer

    def get(self, request, *args, **kwargs):
        timeslot = Timeslots.objects.get(
            pk=kwargs['pk']
        )
        bookings = Booking.objects.filter(
            timeslot_id=timeslot.id
        )
        serializer = BookingsSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListBookingsByUser(generics.ListAPIView):
    """
    Return all bookings made by user
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = BookingsSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
