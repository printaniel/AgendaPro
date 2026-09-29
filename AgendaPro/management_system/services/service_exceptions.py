
class ServiceException(Exception):

    def __init__(self, message = 'Service Exception', status = 200):
        self.message = message
        self.status = status

    def __str__(self):
        return self.message

class AppointmentConflict(ServiceException):

    def __init__(self, message = 'There is an appointment with this data', status = 409):
        super().__init__(message, status)

class ProfessionalDoesNotOfferService(ServiceException):

    def __init__(self, message = 'The professional doesnot offer the service', status = 400):
        super().__init__(message, status)

class InvalidRoleForAppointment (ServiceException):

    def __init__(self, message = 'Invalid user role for appointment', status = 403):
        super().__init__(message, status)

class EntityNotFound(ServiceException):

    def __init__(self, entity, pk, status = 404):
        super().__init__(f'{entity} with id {pk} not found', status) 



