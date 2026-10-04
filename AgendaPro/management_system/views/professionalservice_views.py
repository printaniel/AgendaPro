from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from management_system.serializers import ProfessionalServiceSerializer
from management_system.permissions import IsProfessionalOrAdmin, IsOwnerOrAdmin, IsAppointmentOwnerAdmin
from management_system.models import ProfessionalService
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404


class ProfessionalServiceCreateView(APIView):

    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin]

    def post(self, request):

        serializer = ProfessionalServiceSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save(professional = request.user)
            except IntegrityError as e:
                return Response({"error": "The professional already has a service with this data"}, status = status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST )

class ProfessionalServiceListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProfessionalService.objects.all()
    serializer_class = ProfessionalServiceSerializer


class ProfessionalServiceRetrieveView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = ProfessionalService.objects.all()
    serializer_class = ProfessionalServiceSerializer

class ProfessionalServiceUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin, IsOwnerOrAdmin]

    def patch(self, request, pk):

        professionalservice = get_object_or_404(ProfessionalService, pk = pk)
        self.check_object_permissions(request, professionalservice.professional)
        serializer = ProfessionalServiceSerializer(data = request.data, instance = professionalservice, partial =True)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError as e:
                return Response({"error": "The professional already has a service with this data"}, status = status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class ProfessionalServiceDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin, IsAppointmentOwnerAdmin]
    queryset = ProfessionalService.objects.all()
    serializer_class = ProfessionalServiceSerializer