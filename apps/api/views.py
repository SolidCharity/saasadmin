from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from django.db.models import Q

from apps.api.logic.instances import LogicInstances
from apps.api.logic.products import LogicProducts
from .serializers import InstanceSerializer
from apps.core.models import SaasInstance

class InstanceViewSet(viewsets.ModelViewSet):
    queryset = SaasInstance.objects.all().order_by('id')
    serializer_class = InstanceSerializer
    http_method_names = ['get', 'put']

class InstanceApiView(APIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [TokenAuthentication,SessionAuthentication]

    def getParam(self, request, name, default):
        if len(request.GET) > 0 and name in request.GET:
            return request.GET[name]
        return default

    def get(self, request, *args, **kwargs):
        hostname = self.getParam(request, 'hostname', '')
        product = LogicProducts().get_product(request, False)
        action = self.getParam(request, 'action', '')

        if action == "install":
            instance_status = [SaasInstance().IN_PREPARATION,]
        elif action == "update" or action == "check":
            instance_status = [SaasInstance().READY, SaasInstance().AVAILABLE, SaasInstance().RESERVED, SaasInstance().ASSIGNED, SaasInstance().EXPIRED, SaasInstance().TO_BE_REMOVED,]
        elif action == "remove":
            instance_status = [SaasInstance().TO_BE_REMOVED,]
        else:
            raise Exception('please specify valid action')

        if hostname and product:
            rows = SaasInstance.objects.filter(hostname=hostname, product=product, status__in=instance_status).order_by('id')
        else:
            raise Exception('please specify hostname and product_name')
        serializer = InstanceSerializer(rows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create new instance. assign free instance number
    # test with: {"hostname": "localhost"}
    def put(self, request, *args, **kwargs):
        hostname = self.getParam(request, 'hostname', '')
        product = LogicProducts().get_product(request, False)

        if hostname and product:
            success, new_data = LogicInstances().create_new_instance(hostname, product)
            if success:
                return Response(new_data, status=status.HTTP_201_CREATED)
        else:
            raise Exception('please specify hostname and product_name')

        raise Exception('could not create new instance')

    # update the status of the specified instance
    def patch(self, request, *args, **kwargs):
        hostname = self.getParam(request, 'hostname', '')
        product = LogicProducts().get_product(request, False)
        new_status = self.getParam(request, 'status', '')
        instance_id = self.getParam(request, 'instance_id', '')

        if hostname and product and status and instance_id:
            instance = SaasInstance.objects. \
                filter(Q(identifier=instance_id)&Q(hostname=hostname)&Q(product=product)). \
                first()

        if not instance:
            raise Exception('please specify hostname and product_name and instance_id and status')

        if instance.status == instance.IN_PREPARATION and new_status == instance.READY:
            instance.status = new_status
            instance.save()
            return Response({'success':'true'}, status=status.HTTP_200_OK)

        if instance.status == instance.READY and new_status == instance.AVAILABLE:
            instance.status = new_status
            instance.save()
            return Response({'success':'true'}, status=status.HTTP_200_OK)

        if instance.status == instance.TO_BE_REMOVED and new_status == instance.REMOVED:
            instance.status = new_status
            instance.save()
            return Response({'success':'true'}, status=status.HTTP_200_OK)

        raise Exception('unexpected behaviour')
