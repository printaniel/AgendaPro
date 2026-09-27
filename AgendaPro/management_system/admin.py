from django.contrib import admin
from management_system.models import (
    User,
    ProfessionalProfile,
    CustomerProfile,
    Service,
    ProfessionalService,
    Appointment)


admin.site.register([User, ProfessionalProfile])

