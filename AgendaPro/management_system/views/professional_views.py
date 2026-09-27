from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from management_system.models import User
from management_system.serializers import UserSerializer

class ProfessionalCreateView(APIView):
    
    permission_classes = [AllowAny]  
     
    def post(self, request):
        
        serializer = UserSerializer(data = request.data)     
        if serializer.is_valid():
            serializer.save(role = 'professional')
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    

class ProfessionalListView(ListAPIView):
    permission_classes = [AllowAny]   
    queryset = User.objects.filter(role = 'professional')
    serializer_class = UserSerializer
    
    

class ProfessionalRetrieveView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(role = 'professional')
    serializer_class = UserSerializer

class ProfessionalUpdateView(APIView):
    pass

class ProfessionalDestroyView(APIView):
    pass