from management_system.models import Appointment
from management_system.models import Service, User
from management_system.services.service_exceptions import (
    InvalidRoleForAppointment, 
    ProfessionalDoesNotOfferService,
    EntityNotFound,
    AppointmentConflict)

class AppointmentService:

    @staticmethod
    def create_appointment(user: User, data: dict) -> Appointment :
        professional, customer = AppointmentService._resolve_appointment_actors(user, data)
        service = data.get('service')
        appointment_date = data.get('appointment_date')
        AppointmentService.validate_professional_doesnt_have_service(service = service,professional = professional)  
        return Appointment.objects.create(professional = professional, customer = customer, appointment_date = appointment_date, service = service)

    @staticmethod
    def validate_professional_doesnt_have_service(service:Service, professional: User):
        if not professional.professional_services.filter(service = service).exists():
            raise ProfessionalDoesNotOfferService
    

    @staticmethod
    def _resolve_appointment_actors(user: User, data: dict):
        if not hasattr(user,'role') or user.role not in ['professional', 'customer']:
            raise InvalidRoleForAppointment
        professional = user if user.role == 'professional' else data.get('professional')
        customer = user if user.role == 'customer' else data.get('customer')
        return (professional, customer)

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

    # Refactorizar: No cumple el SRP
    @staticmethod 
    def edit_appointment(appointment: Appointment, data: dict, user: User):
        print(appointment)
        professional, customer =  AppointmentService._resolve_appointment_actors(user, data)
        service = AppointmentService._resolve_appointment_service(appointment, data)

        if not professional:
            professional = appointment.professional
            AppointmentService.validate_professional_doesnt_have_service(service, professional)
            appointment.professional = professional 

        if customer:
            appointment.customer = customer
        appointment.service = service

        appointment.appointment_date = AppointmentService._resolve_appointment_date(appointment, data)
        AppointmentService.validate_unique_appointment(appointment)
        appointment.save()

        
    @staticmethod
    def _resolve_appointment_service(appointment: Appointment, data: dict):
        return data.get('service') if 'service' in data else appointment.service

    @staticmethod
    def _resolve_appointment_date(appointment: Appointment, data: dict):
        return data.get('appointment_date') if 'appointment_date' in data else appointment.appointment_date

    @staticmethod
    def validate_unique_appointment(appointment: Appointment):
           appointments = Appointment.objects.filter(
               professional = appointment.professional, 
               service = appointment.service, 
               appointment_date = appointment.appointment_date,
               cancelled = False).exclude(id = appointment.id)
           if appointments.exists():
               raise AppointmentConflict
