from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from management_system.models import Service
from management_system.serializers import ServiceSerializer

class ServiceCreateView(CreateAPIView):
    permission_classes = []
    #permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceRetrieveView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Service.objects.all()
