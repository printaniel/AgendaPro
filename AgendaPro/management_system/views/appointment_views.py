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
from management_system.services.service_exceptions import (
    ProfessionalDoesNotOfferService,
    InvalidRole,
    EntityNotFound,
    AppointmentConflict,
    MissingRequiredField
    )
from management_system.permissions import IsAppointmentOwnerOrAdmin
from django.db.utils import IntegrityError
from django.db import transaction


class AppointmentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
          
        if request.user.role == 'professional':
            serializer = ProfessionalAppointmentSerializer(data = request.data)
        elif request.user.role == 'customer':
            serializer = CustomerAppointmentSerializer(data = request.data)
        else:
            return Response({"error": f"Role {request.user.role} cannot create appointments"}, status = status.HTTP_403_FORBIDDEN)
            
            
        if serializer.is_valid():

            try:
                with transaction.atomic():
                    appointment = AppointmentService.create_appointment(request.user, serializer.validated_data)
                    read_serializer = ReadAppointmentSerializer(instance = appointment)
                return Response(read_serializer.data, status = status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({"error":"Appointment cannot be created"}, status = status.HTTP_409_CONFLICT)
            except (ProfessionalDoesNotOfferService, InvalidRole, MissingRequiredField) as e:
                return Response({"error": str(e)}, status = e.status)
                
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
        
        try:
            appointment = AppointmentService.get_not_cancelled_appointment(pk)
        except EntityNotFound as e:
            return Response({"error":str(e)}, status = e.status)
        
        self.check_object_permissions(request, appointment)
        serializer = AppointmentUpdateSerializer(instance = appointment, data = request.data, partial = True)
        
        if serializer.is_valid():
            try:
                AppointmentService.edit_appointment(appointment, serializer.validated_data, request.user)
                read_serializer_result = ReadAppointmentSerializer(instance = appointment)
            except (AppointmentConflict, InvalidRole) as e:
                return Response({"error": str(e)}, status = e.status)  
            except IntegrityError:
                return Response({"error":"Appointment cannot be created"}, status = status.HTTP_409_CONFLICT)        
            return Response(read_serializer_result.data,status = status.HTTP_200_OK)
        else:
            return Response({"error":serializer.errors}, status = status.HTTP_400_BAD_REQUEST)


class AppointmentCancelView(APIView):

    permission_classes = [IsAuthenticated, IsAppointmentOwnerOrAdmin]
    def patch(self, request, pk):
        try:
            appointment = AppointmentService.get_not_cancelled_appointment(pk)
        except EntityNotFound as e:
            return Response({"error":str(e)}, status = e.status)

        self.check_object_permissions(request, appointment)

        AppointmentService.cancel_appointment(appointment)
        return Response({"message": f"Appointment with id {pk} has been cancelled"}, status = status.HTTP_200_OK)
        
        
        