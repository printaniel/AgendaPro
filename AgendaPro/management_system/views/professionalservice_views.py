from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from management_system.serializers import ProfessionalServiceSerializer, ProfessionalServiceCreateSerializer
from management_system.permissions import IsProfessionalOrAdmin, IsProfessionalServiceOwnerOrAdmin
from management_system.models import ProfessionalService
from django.shortcuts import get_object_or_404


class ProfessionalServiceCreateView(APIView):

    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin]

    def post(self, request):

        serializer = ProfessionalServiceCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(professional = request.user)
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
    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin, IsProfessionalServiceOwnerOrAdmin]

    def patch(self, request, pk):

        professionalservice = get_object_or_404(ProfessionalService, pk = pk)
        self.check_object_permissions(request, professionalservice)
        serializer = ProfessionalServiceSerializer(data = request.data, instance = professionalservice, partial =True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class ProfessionalServiceDestroyView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin, IsProfessionalServiceOwnerOrAdmin]
    queryset = ProfessionalService.objects.all()
