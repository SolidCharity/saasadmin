from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from .serializers import InstanceSerializer
from apps.core.models import SaasInstance

class InstanceViewSet(viewsets.ModelViewSet):
    queryset = SaasInstance.objects.all().order_by('id')
    serializer_class = InstanceSerializer
    #http_method_names = ['get', 'post']

class InstanceApiView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        rows = SaasInstance.objects.all().order_by('id')
        serializer = InstanceSerializer(rows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        data = {
            'identifier': request.data.get('identifier'),
            'hostname': request.data.get('hostname'),
            'status': request.data.get('status'),
        }
        serializer = InstanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
