from  rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from management_system.models import User
from management_system.serializers import UserSerializer
from management_system.services.customer_services import CustomerServices
from management_system.services.professional_services import ProfessionalServices


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleSeparetedUserListView(APIView):

    def get(self, request):

        professionals = ProfessionalServices.get_professionals()
        customers = CustomerServices.get_customers()
        customer_serializer = UserSerializer(data = customers, many = True)
        professional_serializer = UserSerializer(data = professionals, many = True)

        return Response({'professionals': professional_serializer, 'customers': customer_serializer})
    