from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from management_system.serializers import ProfessionalServiceSerializer
from management_system.permissions import IsProfessionalAdmin, IsSameUserAdmin
from management_system.models import ProfessionalService
from django.db.utils import IntegrityError

class ProfessionalServiceCreateView(APIView):

    permission_classes = []

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

class ProfessionalServiceUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsProfessionalAdmin, IsSameUserAdmin]
    queryset = ProfessionalService.objects.all()
    serializer_class = ProfessionalServiceSerializer

class ProfessionalServiceDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsProfessionalAdmin, IsSameUserAdmin]
    queryset = ProfessionalService.objects.all()
    serializer_class = ProfessionalServiceSerializer