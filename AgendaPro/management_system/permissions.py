from rest_framework.permissions import BasePermission
from management_system.models import Appointment, ProfessionalService

class IsProfessionalOrAdmin(BasePermission):
    
    def has_permission(self, request, view):

        if request.user.is_staff:
            return True        
        if request.user.role == 'professional':
            return True       
        return False

class IsCustomerOrAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_staff:
            return True
        if request.user.role == 'customer':
            return True
        return False
    
class IsOwnerOrAdmin(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
             return True      
        return request.user == obj

class IsAppointmentOwnerAdmin(BasePermission):

    def has_object_permission(self, request, view, appointment: Appointment):
        if request.user.is_staff:
            return True

        return request.user == appointment.professional or request.user == appointment.customer
    
class IsProfessionalServiceOwnerAdmin(BasePermission):
    
    def has_object_permission(self, request, view, professional_service: ProfessionalService):
        if request.user.is_staff:
            return True
        
        return request.user == professional_service.professional