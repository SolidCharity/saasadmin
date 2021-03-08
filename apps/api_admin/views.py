from rest_framework import viewsets

from .serializers import SaaSInstanceSerializer
from apps.backend.models import SaaSInstance


class SaaSInstanceViewSet(viewsets.ModelViewSet):
    queryset = SaasInstance.objects.all().order_by('id')
    serializer_class = SaaSInstanceSerializer
