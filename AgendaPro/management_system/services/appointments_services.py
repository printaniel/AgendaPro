from management_system.models import Appointment
from management_system.models import Service, User
from management_system.services.service_exceptions import (
    ProfessionalDoesNotOfferService,
    EntityNotFound,
    AppointmentConflict,
    InvalidRole,
    MissingRequiredField)
from datetime import datetime, timedelta
from django.db import transaction
from django.utils import timezone

LATE_CANCELLED_TIME = timedelta(days = 2)

class AppointmentService:
    
    @staticmethod
    def create_appointment(user: User, data: dict) -> Appointment :
        professional, customer, service, appointment_date  = AppointmentService._resolve_all_for_create(user, data)
        AppointmentService.ensure_professional_offers_service(service = service,professional = professional)  
        return Appointment.objects.create(professional = professional, customer = customer, appointment_date = appointment_date, service = service)
    
    @staticmethod 
    def edit_appointment(appointment: Appointment, data: dict, user: User):
        AppointmentService._validate_customer_professional_role(user)
        appointment.appointment_date = data.get("appointment_date") if 'appointment_date' in data else appointment.appointment_date
        AppointmentService._validate_unique_appointment(appointment)
        appointment.save()

    @staticmethod
    @transaction.atomic
    def cancel_appointment(appointment: Appointment, now = None):     
        now = now or timezone.now()
        late_cancelled = appointment.appointment_date - now < LATE_CANCELLED_TIME
        if late_cancelled: 
            appointment.status = appointment.Status.LATE_CANCELLED
        else:
            appointment.status = appointment.Status.CANCELLED
        appointment.cancelled_at = now
        appointment.save(update_fields=["status", "cancelled_at"])

    @staticmethod
    def get_not_cancelled_appointment(appointment_id: int):
        appointment = Appointment.objects.filter(id = appointment_id, status = 'confirmed').first()
        if not appointment:
            raise EntityNotFound('not cancelled appointment', appointment_id)
        return appointment

    @staticmethod
    def get_appointment(appointment_id: int):
        appointment = Appointment.objects.filter(id = appointment_id).first()
        if not appointment:
            raise EntityNotFound('appointment', appointment_id)
        return appointment
        
    @staticmethod
    def _resolve_all_for_update(user: User, data: dict, appointment: Appointment) -> tuple[User, User, Service, datetime]:
        
        appointment_date = data.get('appointment_date',appointment.appointment_date)
        service = data.get('service', appointment.service)
        
        if 'professional' in data and data.get('professional') is not None:
            professional = data.get('professional')
        else:
            professional = appointment.professional
            
        if 'customer' in data and data.get('customer') is not None:
            customer = data.get('customer')
        else: 
            customer = appointment.customer
        return (professional, customer, service, appointment_date)
    
    def _validate_customer_professional_role(user: User):
        if not user or user.role not in ['professional', 'customer']:
            raise InvalidRole('create appointment')
         
    def _validate_unique_appointment(appointment: Appointment):
        appointments = Appointment.objects.filter(
            professional = appointment.professional, 
            service = appointment.service, 
            appointment_date = appointment.appointment_date,
            cancelled_at = None).exclude(id = appointment.id)
        if appointments.exists():
            raise AppointmentConflict

    def ensure_professional_offers_service(service:Service, professional: User):
        if not professional.professional_services.filter(service = service).exists():
            raise ProfessionalDoesNotOfferService
    
    def _resolve_all_for_create(user: User, data: dict):       
        service = data.get('service')
        professional = user if user.role == 'professional' else data.get('professional')
        customer = user if user.role == 'customer' else data.get('customer')
        appointment_date = data.get('appointment_date')
        return (professional, customer, service, appointment_date)