from management_system.models import User, Service
from management_system.services.service_exceptions import EntityNotFound

class ProfessionalServices:

    @staticmethod
    def list_professionals():
        return User.objects.filter(role = 'professional')
    
    @staticmethod
    def get_active_by_id(id: int):
        user = User.objects.filter(role = 'professional', id = id).first()
        if not user:
            raise EntityNotFound('professional', id)
        return user

    @staticmethod
    def deactivate(user: User):
        user.is_active = False
        user.save()