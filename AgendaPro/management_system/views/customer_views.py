from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from management_system.serializers import UserSerializer
from management_system.models import User


class CustomerCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        serializer = UserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save(role = 'customer')
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status = status.HTTP_400_BAD_REQUEST )

class CustomerListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(role = 'customer')
    serializer_class = UserSerializer

class CustomerRetrieveView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(role = 'customer')
    serializer_class = UserSerializer

class CustomerUpdateView(UpdateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(role = 'customer')
    serializer_class = UserSerializer

class CustomerDestroyView(DestroyAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.filter(role = 'customer')
    serializer_class = UserSerializer
