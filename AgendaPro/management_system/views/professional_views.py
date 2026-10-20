from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from management_system.models import User
from management_system.serializers import UserSerializer, PublicProfessionalSerializer
from management_system.permissions import IsProfessionalOrAdmin, IsOwnerOrAdmin
from management_system.services.professional_services import ProfessionalServices
from management_system.services.service_exceptions import EntityNotFound

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
    serializer_class = PublicProfessionalSerializer
    
class ProfessionalRetrieveView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(role = 'professional')
    serializer_class = PublicProfessionalSerializer

class ProfessionalUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin, IsOwnerOrAdmin]
    queryset = User.objects.filter(role = 'professional')
    serializer_class = UserSerializer

class ProfessionalDestroyView(APIView):
    permission_classes = [IsAuthenticated, IsProfessionalOrAdmin, IsOwnerOrAdmin]
    
    def delete(self, request, pk):

        try:
            user = ProfessionalServices.get_active_by_id(pk)
        except EntityNotFound as e:
            return Response({"error":str(e)}, status = e.status)
        
        ProfessionalServices.deactivate(user)
        return Response(status = status.HTTP_200_OK)
        
