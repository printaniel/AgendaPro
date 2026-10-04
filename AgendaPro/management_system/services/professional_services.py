from management_system.models import User, Service


class ProfessionalServices:

    @staticmethod
    def get_professionals():
        return User.objects.filter(role = 'professional')

    @staticmethod
    def get_professional(id):
        return User.objects.filter(role = 'professional', id = id)

    
    