from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from management_system.serializers import AppointmentSerializer
from management_system.models import Appointment
from management_system.services.appointments_services import AppointmentsService
from management_system.services.service_exceptions import (
    ProfessionalDoesNotOfferService,
    InvalidRoleForAppointment,
    EntityNotFound)
from management_system.permissions import IsAppointmentoOwnerAdmin
from django.db.utils import IntegrityError
from django.db import transaction


class AppointmentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
           
            serializer = AppointmentSerializer(data = request.data)
            if serializer.is_valid():

                try:
                    with transaction.atomic():   
                        appointment = AppointmentsService.create_appointment(request.user, serializer.validated_data)
                        read_serializer = AppointmentSerializer(instance = appointment)
                    return Response(read_serializer.data, status = status.HTTP_201_CREATED)
                except IntegrityError:
                    return Response({"error":"Appointment cannot be created"})
                except (ProfessionalDoesNotOfferService, InvalidRoleForAppointment) as e:
                    return Response({"error": str(e)}, status = e.status)
                
            return Response({"error": serializer.errors})


class AppointmentListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsAppointmentoOwnerAdmin]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

class AppointmentUpdateView(APIView):
    """
    Solo un usuario Customer o Professional asociados a la cita pueden acceder a editarla
    Se debe validar que dicho usuario brinde dicho servicio 
    """

    pass

class AppointmentCancelView(APIView):

    permission_classes = [IsAuthenticated, IsAppointmentoOwnerAdmin]
    def delete(self, request, pk):
        try:
            appointment = AppointmentsService.get_not_cancelled_appointment(pk)
        except EntityNotFound as e:
            return Response({"error":str(e)}, status = e.status)

        self.check_object_permissions(request, appointment)

        AppointmentsService.cancel_appointment(appointment)
        return Response({"message": f"Appointment with id {pk} has been cancelled"}, status = status.HTTP_200_OK)
        