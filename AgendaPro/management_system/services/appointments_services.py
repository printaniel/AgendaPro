from management_system.models import Appointment
from management_system.models import Service, User
from management_system.services.service_exceptions import (
    ProfessionalDoesNotOfferService,
    EntityNotFound,
    AppointmentConflict)
from datetime import datetime

class AppointmentService:

    @staticmethod
    def create_appointment(user: User, data: dict) -> Appointment :
        professional, customer, service, appointment_date  = AppointmentService._resolve_all(user, data, None)
        AppointmentService.validate_professional_doesnt_have_service(service = service,professional = professional)  
        return Appointment.objects.create(professional = professional, customer = customer, appointment_date = appointment_date, service = service)

    @staticmethod
    def validate_professional_doesnt_have_service(service:Service, professional: User):
        if not professional.professional_services.filter(service = service).exists():
            raise ProfessionalDoesNotOfferService

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
    def edit_appointment(appointment: Appointment, data: dict, user: User):

        professional, customer, service, appointment_date = AppointmentService._resolve_all(user, data, appointment)
        AppointmentService.validate_professional_doesnt_have_service(service, professional)
        appointment.professional = professional
        appointment.customer = customer
        appointment.service = service
        appointment.appointment_date = appointment_date
        AppointmentService.validate_unique_appointment(appointment)
        appointment.save()

    @staticmethod
    def validate_unique_appointment(appointment: Appointment):
           appointments = Appointment.objects.filter(
               professional = appointment.professional, 
               service = appointment.service, 
               appointment_date = appointment.appointment_date,
               cancelled = False).exclude(id = appointment.id)
           if appointments.exists():
               raise AppointmentConflict 
           
    @staticmethod
    def _resolve_all(user: User, data: dict, appointment: Appointment) -> User|User|Service|datetime:
        
        appointment_date = data.get('appointment_date',appointment.appointment_date)
        service = data.get('service', appointment.service)
        professional = user if user.role == 'professional' else data.get('professional', appointment.professional)
        customer = user if user.role == 'customer' else data.get('customer', appointment.customer)
        return (professional, customer, service, appointment_date)
