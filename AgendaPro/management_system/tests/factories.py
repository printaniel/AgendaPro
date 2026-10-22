import factory
from factory.django import DjangoModelFactory
from management_system.models import (User, Service)

DEFAULT_PASSWORD = 'hesoyam2'

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = DEFAULT_PASSWORD
    role = 'customer'
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = cls._get_manager(model_class).create_user(*args, **kwargs)
        user.raw_password = DEFAULT_PASSWORD
        return user
    
class ProfessionalFactory(UserFactory):    
    role = 'professional'
    
class CustomerFactory(UserFactory):
    role = 'customer'
    
class AdminFactory(UserFactory):
  
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_superuser(*args, **kwargs)
    
class ServiceFactory(DjangoModelFactory):
    class Meta:
        model = Service
    
    service_name = factory.Sequence(lambda n: f"service{n}")
