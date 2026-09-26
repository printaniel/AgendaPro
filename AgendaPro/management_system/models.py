from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE = [("professional","Professional"), ("customer", "Customer")]
    role = models.CharField(max_length = 50,choices = ROLE)
    
    
class ProfessionalProfile(models.Model):  
    bio = models.CharField(max_length= 300)
    avatar = models.ImageField(upload_to= 'avatars/', blank = True, null = True)
    
class CustomerProfile(models.Model):
    avatar = models.ImageField(upload_to= 'avatars/', blank = True, null = True)
    
class Service(models.Model):
    service_name = models.CharField(max_length = 50)
    professionals = models.ManyToManyField(User, through = 'ProfessionalService', related_name = 'services')

    def __str__(self):
        return self.service_name
    
class ProfessionalService(models.Model): 
    professional = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'professional_services')
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    duration = models.DurationField()
    description = models.TextField()

    class Meta:
        unique_together = ['professional', 'service','price','duration']

    def __str__(self):
        return f"{self.professional.username} - {self.service.service_name}"

class Appointment(models.Model): 

    cancelled = models.BooleanField(default = False)
    late_cancelled = models.BooleanField(default = False)
    customer = models.ForeignKey(User, on_delete = models.CASCADE)
    professional = models.ForeignKey(User, on_delete = models.CASCADE)
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    appointment_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields = ['appointment_date','professional', 'service'],
            condition = models.Q(cancelled = False),
            name = 'unique_appointment_slot'
            ) ]
        
    def __str__(self):
        return f"Cita: {self.customer.username} - {self.professional.username} - {self.service.service_name} - {self.appointment_date}"
