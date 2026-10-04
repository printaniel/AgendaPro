
class ServiceException(Exception):
    def __init__(self, message = 'Service Exception', status = 406):
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

class InvalidRole(ServiceException):
    def __init__(self, action, status = 403):
        super().__init__(message = f'Invalid user role for this action {action}', status = 403)

class EntityNotFound(ServiceException):
    def __init__(self, entity, pk, status = 404):
        super().__init__(f'{entity} with id {pk} not found', status) 

class MissingRequiredField(ServiceException):    
    def __init__(self, field):
        super().__init__(message = f'Missing required field {field}')
        
class NotAllowedAction(ServiceException):
    def __init__(self, action):
        super().__init__(message = f'You are not allowed to do this action {action}', status = 403)

