from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from management_system.serializers import UserSerializer
from management_system.models import User
from management_system.permissions import IsCustomerOrAdmin, IsOwnerOrAdmin
from management_system.services.customer_services import CustomerServices
from management_system.services.service_exceptions import EntityNotFound


class CustomerCreateView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(role = 'customer')
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status = status.HTTP_400_BAD_REQUEST )

class CustomerListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = User.objects.filter(role = 'customer')
    serializer_class = UserSerializer

class CustomerRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsCustomerOrAdmin, IsOwnerOrAdmin]
    queryset = User.objects.filter(role = 'customer')
    serializer_class = UserSerializer

class CustomerUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCustomerOrAdmin, IsOwnerOrAdmin]
    queryset = User.objects.filter(role = 'customer')
    serializer_class = UserSerializer

class CustomerDestroyView(APIView):
    permission_classes = [IsAuthenticated, IsCustomerOrAdmin, IsOwnerOrAdmin]
    
    def delete(self, request, pk):

        try:
           customer = CustomerServices.get_active_customer_by_id(pk)
        except EntityNotFound as e:
            return Response({"error": str(e)}, status = e.status)
        
        self.check_object_permissions(request, customer)
        CustomerServices.deactivate(customer)
        return Response(status = status.HTTP_204_NO_CONTENT)


