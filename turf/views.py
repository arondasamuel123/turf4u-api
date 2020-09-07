from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from turfapi.models import Turf, Organization, User
from .serializers import TurfSerializer, OrgSerializer
from .permissions import IsTurfManager


class ListTurfs(generics.ListAPIView):
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


class CreateTurf(generics.CreateAPIView):
    """
    API View to create and list out turfs
    """
    queryset = Turf.objects.all()
    serializer_class = TurfSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsTurfManager]

    def create(self, request, pk):
        organization = Organization.objects.get(pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(org=organization)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveTurfByOrg(generics.RetrieveAPIView):
    """
    API View to list turfs asscoicated to
    an organization
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsTurfManager, ]

    def get(self, request, pk):
        organization = Organization.objects.get(pk=pk)
        turfs = Turf.objects.filter(org_id=organization.id).all()
        serializer = TurfSerializer(turfs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrg(generics.CreateAPIView):
    """
    API view to create an organization
    """
    queryset = Organization.objects.all()
    serializer_class = OrgSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsTurfManager, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateOrg(generics.RetrieveUpdateAPIView):
    """
    API to get and update organization by ID
    """
    serializer_class = OrgSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsTurfManager]
    queryset = Organization.objects.all()


class RetrieveOrgByUser(generics.RetrieveAPIView):
    """
    API view to get organization by authenticated user
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsTurfManager]

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        organizations = Organization.objects.filter(user_id=user.id).all()
        serializer = OrgSerializer(organizations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
