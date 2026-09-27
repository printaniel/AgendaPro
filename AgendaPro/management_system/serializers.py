from rest_framework import serializers
from management_system.models import User, Service

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only = True)
    email = serializers.EmailField(required = True)
    id = serializers.IntegerField(read_only = True)
    
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email']
        
    def create(self, validated_data):       
        password = validated_data.pop("password")
        user = User.objects.create_user(password = password, **validated_data)
        return user

    def update(self, instance: User, validated_data):
        
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        if 'username' in validated_data:
            instance.username = validated_data.pop('username')

        if 'email' in validated_data:
            instance.email = validated_data.pop('email')

        instance.save()

        return instance

class ServiceSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only = True)

    class Meta:
        model = Service
        fields = ['id','service_name']
