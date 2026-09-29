from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from management_system.serializers import (
    AppointmentSerializer, 
    AppointmentOnlyReadSerializer
)
from management_system.models import Appointment
from management_system.services.appointments_services import AppointmentsService
from management_system.services.service_exceptions import ProfessionalDoesNotOfferService, InvalidRoleForAppointment
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


class AppointmentRetrieveView(APIView):
    pass

class AppointmentUpdateView(APIView):
    pass

class AppointmentDestroyView(APIView):
    pass