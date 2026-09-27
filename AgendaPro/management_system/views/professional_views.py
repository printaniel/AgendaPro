from rest_framework.views import APIView
from management_system.models import User
from management_system.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status

class ProfessionalCreateView(APIView):
    
    def post(self, request):
        
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save(role = 'professional')
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    

class ProfessionalListView(APIView):
    pass

class ProfessionalRetrieveView(APIView):
    pass

class ProfessionalUpdateView(APIView):
    pass

class ProfessionalDestroyView(APIView):
    pass