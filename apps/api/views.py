from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from apps.api.logic.instances import LogicInstances
from .serializers import InstanceSerializer
from apps.core.models import SaasInstance

class InstanceViewSet(viewsets.ModelViewSet):
    queryset = SaasInstance.objects.all().order_by('id')
    serializer_class = InstanceSerializer
    http_method_names = ['get', 'put']

class InstanceApiView(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def get(self, request, *args, **kwargs):
        if len(request.GET) > 0 and 'hostname' in request.GET:
            hostname = request.GET['hostname']
            rows = SaasInstance.objects.filter(hostname=hostname).order_by('id')
        else:
            rows = SaasInstance.objects.all().order_by('id')
        serializer = InstanceSerializer(rows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create new instance. assign free instance number
    # test with: {"hostname": "localhost"}
    def put(self, request, *args, **kwargs):
        if len(request.data) > 0 and 'hostname' in request.data:
            hostname = request.data['hostname']
        else:
            hostname = 'localhost'

        success, new_data = LogicInstances().create_new_instance(hostname)
        if success:
            return Response(new_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
