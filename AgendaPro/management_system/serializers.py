from rest_framework import serializers
from management_system.models import User

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True)
    email = serializers.EmailField(required = True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        
    def create(self, validated_data):
        
        password = validated_data.pop("password")
        user = User.objects.create_user(password = password, **validated_data)
        return user