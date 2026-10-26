from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from management_system.serializers import (
    CustomerAppointmentSerializer,
    ProfessionalAppointmentSerializer,
    AppointmentUpdateSerializer,
    ReadAppointmentSerializer,
    BaseAppointmentSerializer
    )
from management_system.models import Appointment
from management_system.services.appointments_services import AppointmentService
from management_system.services.service_exceptions import InvalidRole
from management_system.permissions import IsAppointmentOwnerOrAdmin
from django.db import transaction


class AppointmentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
          
        if request.user.role == 'professional':
            serializer = ProfessionalAppointmentSerializer(data = request.data)
        elif request.user.role == 'customer':
            serializer = CustomerAppointmentSerializer(data = request.data)
        else:
            raise InvalidRole()
                    
        if serializer.is_valid():
            with transaction.atomic():
                appointment = AppointmentService.create_appointment(request.user, serializer.validated_data)
            read_serializer = ReadAppointmentSerializer(instance = appointment)
            return Response(read_serializer.data, status = status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class AppointmentListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Appointment.objects.all()
    serializer_class = BaseAppointmentSerializer


class AppointmentRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrAdmin]
    queryset = Appointment.objects.all()
    serializer_class = BaseAppointmentSerializer

class AppointmentUpdateView(APIView):

    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrAdmin]

    def patch(self, request, pk):
        appointment = AppointmentService.get_not_cancelled_appointment(pk)
        
        self.check_object_permissions(request, appointment)
        serializer = AppointmentUpdateSerializer(instance = appointment, data = request.data, partial = True)
        
        if serializer.is_valid():
            AppointmentService.edit_appointment(appointment, serializer.validated_data, request.user)
            read_serializer_result = ReadAppointmentSerializer(instance = appointment)    
            return Response(read_serializer_result.data,status = status.HTTP_200_OK)
        else:
            return Response({"error":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class AppointmentCancelView(APIView):

    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrAdmin]
    def patch(self, request, pk):
        appointment = AppointmentService.get_not_cancelled_appointment(pk)

        self.check_object_permissions(request, appointment)

        AppointmentService.cancel_appointment(appointment)
        return Response({"message": f"Appointment with id {pk} has been cancelled"}, status = status.HTTP_200_OK)
        
        
        