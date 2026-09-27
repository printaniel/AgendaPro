from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from management_system.serializers import ProfessionalServiceSerializer
from management_system.permissions import IsProfessionalAdmin

class ProfessionalServiceCreateView(APIView):

    permission_classes = []

    def post(self, request):

        serializer = ProfessionalServiceSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(professional = request.user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status = status.HTTP_400_BAD_REQUEST )

class ProfessionalServiceListView(APIView):
    pass

class ProfessionalServiceRetrieveView(APIView):
    pass

class ProfessionalServiceUpdateView(APIView):
    pass

class ProfessionalServiceDestroyView(APIView):
    pass