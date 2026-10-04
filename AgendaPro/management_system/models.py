from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE = [("professional","Professional"), ("customer", "Customer")]
    role = models.CharField(max_length = 50,choices = ROLE)
    
    def __str__(self):
        return self.username
    
class ProfessionalProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    bio = models.CharField(max_length= 300)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
        
class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
    
class Service(models.Model):
    service_name = models.CharField(max_length = 50)
    professional = models.ManyToManyField(User, through = 'ProfessionalService', related_name = 'services')

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
    customer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'appointments_as_customer')
    professional = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'appointments_as_professional')
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    create_at = models.DateTimeField(auto_now_add = True)
    appointment_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields = ['appointment_date','professional', 'service'],
            condition = models.Q(cancelled = False),
            name = 'unique_appointment_slot'
            ) ]
        
    def __str__(self):
        return f"Appointment: {self.customer.username} - {self.professional.username} - {self.service.service_name} - {self.appointment_date}"
