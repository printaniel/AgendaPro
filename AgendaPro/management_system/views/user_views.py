from  rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from management_system.models import User
from management_system.serializers import UserSerializer, PrivateProfessionalSerializer


class UserListView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleSeparetedUserListView(APIView):

    permission_classes = [IsAdminUser]
    def get(self, request):

        professionals = User.objects.professionals()
        customers = User.objects.customers()

        customer_serializer = UserSerializer(customers, many = True)
        professional_serializer = PrivateProfessionalSerializer(professionals, many = True)

        return Response({'professionals': professional_serializer.data, 'customers': customer_serializer.data})
    