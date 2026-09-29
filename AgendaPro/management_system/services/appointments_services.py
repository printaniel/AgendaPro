from management_system.models import Appointment
from management_system.models import Service, User
from management_system.services.service_exceptions import (
    InvalidRoleForAppointment, 
    ProfessionalDoesNotOfferService,
    EntityNotFound)

class AppointmentsService:

    @staticmethod
    def create_appointment(user: User, data: dict) -> Appointment :
        professional, customer = AppointmentsService._resolve_appointment_actors(user, data)
        service = data.get('service')
        appointment_date = data.get('appointment_date')
        AppointmentsService.validate_professional_doesnt_have_service(service = service,professional = professional)
    
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
    def get_not_cancelled_appointment(pk):
        appointment = Appointment.objects.filter(id = pk, cancelled = False).first()
        if not appointment:
            raise EntityNotFound('not cancelled appointment', pk)
        return appointment
