class DomainException(Exception):
    code = 'domain_error'
    default_message = 'Domain error'
    def __init__(self, message = None):
        self.default_message = message if message else self.default_message
        super().__init__(self.default_message)
        

class AppointmentConflict(DomainException):
    code = 'appointment_conflict'
    default_message = 'There is an appointment with this data'
    
class ProfessionalDoesNotOfferService(DomainException):
    code = 'service_not_offered'
    default_message = 'The professional doesnot offer the service'


class InvalidRole(DomainException):
    code = 'invalid_role'
    default_message = 'Invalid user role for this action'

class EntityNotFound(DomainException):
    code = 'entity_not_found'
    def __init__(self, entity, pk, status = 404):
        super().__init__(f'{entity} with id {pk} not found', status) 
        
class NotAllowedAction(DomainException):
    code = 'not_allowed'
    default_message = 'You are not allowed to do this action '

