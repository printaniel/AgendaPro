from rest_framework.permissions import BasePermission

class IsProfessionalAdmin(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.user.is_staff:
            return True 
        
        if not request.user.role == 'professional':
            return True
        
        return False