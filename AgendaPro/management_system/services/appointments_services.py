from management_system.models import Appointment
from management_system.models import Service, User
from management_system.services.service_exceptions import (
    ProfessionalDoesNotOfferService,
    EntityNotFound,
    AppointmentConflict,
    InvalidRole,
    MissingRequiredField,
    NotAllowedAction)
from datetime import datetime

class AppointmentService:

    @staticmethod
    def create_appointment(user: User, data: dict) -> Appointment :
        AppointmentService._validate_customer_professional_role(user)
        AppointmentService._validate_required_actor_fields(user, data)
        professional, customer, service, appointment_date  = AppointmentService._resolve_all_for_create(user, data)
        AppointmentService.validate_professional_doesnt_have_service(service = service,professional = professional)  
        return Appointment.objects.create(professional = professional, customer = customer, appointment_date = appointment_date, service = service)
    
    @staticmethod 
    def edit_appointment(appointment: Appointment, data: dict, user: User):
        AppointmentService._validate_customer_professional_role(user)
        AppointmentService._validate_actor_cannot_change_own_role_field (user, data)
        professional, customer, service, appointment_date = AppointmentService._resolve_all_for_update(user, data, appointment)
        AppointmentService._validate_professional_doesnt_have_service(service, professional)
        appointment.professional = professional
        appointment.customer = customer
        appointment.service = service
        appointment.appointment_date = appointment_date
        AppointmentService._validate_unique_appointment(appointment)
        appointment.save()

    @staticmethod
    def cancel_appointment(appointment: Appointment):
        appointment.cancelled = True
        appointment.save()

    @staticmethod
    def get_not_cancelled_appointment(appointment_id: int):
        appointment = Appointment.objects.filter(id = appointment_id, cancelled = False).first()
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
        
    def _validate_required_actor_fields(user: User, data: dict):
        if user.role == 'customer' and not data.get('professional'):
            raise MissingRequiredField('professional')
        if user.role == 'professional' and not data.get('customer'):
            raise MissingRequiredField('customer')
        
    def _validate_actor_cannot_change_own_role_field (user: User, data: dict):
        if user.role == 'customer' and data.get('customer'):
            raise NotAllowedAction('edit customer')
        elif user.role == 'professional' and data.get('professional'):
            raise NotAllowedAction('edit professional')
    
    def _validate_unique_appointment(appointment: Appointment):
        appointments = Appointment.objects.filter(
            professional = appointment.professional, 
            service = appointment.service, 
            appointment_date = appointment.appointment_date,
            cancelled = False).exclude(id = appointment.id)
        if appointments.exists():
            raise AppointmentConflict

    def _validate_professional_doesnt_have_service(service:Service, professional: User):
        if not professional.professional_services.filter(service = service).exists():
            raise ProfessionalDoesNotOfferService  
    
    def _resolve_all_for_create(user: User, data: dict):       
        service = data.get('service')
        professional = user if user.role == 'professional' else data.get('professional')
        customer = user if user.role == 'customer' else data.get('customer')
        appointment_date = data.get('appointment_date')
        return (professional, customer, service, appointment_date)