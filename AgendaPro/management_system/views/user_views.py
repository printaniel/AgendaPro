from  rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from management_system.models import User
from management_system.serializers import UserSerializer, PrivateProfessionalSerializer
from management_system.services.customer_services import CustomerServices
from management_system.services.professional_services import ProfessionalServices


class UserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleSeparetedUserListView(APIView):

    permission_classes = [IsAdminUser]
    def get(self, request):

        professionals = ProfessionalServices.get_professionals()
        customers = CustomerServices.get_customers()

        customer_serializer = UserSerializer(customers, many = True)
        professional_serializer = PrivateProfessionalSerializer(professionals, many = True)

        return Response({'professionals': professional_serializer.data, 'customers': customer_serializer.data})
    