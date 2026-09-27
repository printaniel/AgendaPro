from rest_framework.permissions import BasePermission

class IsProfessionalAdmin(BasePermission):
    
    def has_permission(self, request, view):
        print("Intento de probar si es profesional")
        print(request.user.role)
        if request.user.is_staff:
            return True        
        if request.user.role == 'professional':
            print("Es professional")
            return True       
        return False
    
class IsSameUserAdmin(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.is_staff:
             return True      
        return request.user == obj