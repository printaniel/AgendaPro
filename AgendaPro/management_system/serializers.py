from rest_framework import serializers
from management_system.models import User

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']