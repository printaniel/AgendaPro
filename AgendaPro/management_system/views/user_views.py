from  rest_framework.generics import ListAPIView#
from management_system.models import User
from management_system.serializers import UserSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    