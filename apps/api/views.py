from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .serializers import SaaSInstanceSerializer
from apps.backend.models import SaaSInstance

class SaaSInstanceViewSet(viewsets.ModelViewSet):
    queryset = SaaSInstance.objects.all().order_by('id')
    serializer_class = SaaSInstanceSerializer

class SaaSInstanceApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rows = SaaSInstance.objects.all().order_by('id')
        serializer = SaaSInstanceSerializer(rows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        data = {
            'hostname': request.data.get('hostname'),
            'status': request.data.get('status'),
        }
        serializer = SaaSInstanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
