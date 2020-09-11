from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from turfapi.models import Turf, Timeslots
from .serializers import TimeslotsSerializer


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
