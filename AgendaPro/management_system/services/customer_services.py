from management_system.models import User
from management_system.services.service_exceptions import EntityNotFound

class CustomerServices:

    @staticmethod
    def get_customers():
        return User.objects.filter(role = 'customer')

    @staticmethod
    def deactivate(customer: Customer):
        customer.is_active = False
        customer.save()

    @staticmethod
    def get_active_customers():
        return User.objects.filter( role = 'customer', is_active = True)

    @staticmethod
    def get_active_customer_by_id(id: int):
        user = User.objects.filter(id = id ,role = 'customer', is_active = True)
        if not user:
            raise EntityNotFound("customer", id)
        return user
