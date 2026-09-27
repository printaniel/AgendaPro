from management_system.models import User

class ProfessionalServices:

    @staticmethod
    def get_professionals():
        return User.objects.filter(role = 'professional')