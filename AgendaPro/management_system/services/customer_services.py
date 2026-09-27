from management_system.models import User

class CustomerServices:

    @staticmethod
    def get_customers():
        return User.objects.filter(role = 'customer')