from rest_framework.permissions import BasePermission

class IsProfessionalAdmin(BasePermission):
    
    def has_permission(self, request, view):

        if request.user.is_staff:
            return True        
        if request.user.role == 'professional':
            return True       
        return False

class IsCustomerAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_staff:
            return True
        if request.user.role == 'customer':
            return True
        return False
    
class IsSameUserAdmin(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
             return True      
        return request.user == obj