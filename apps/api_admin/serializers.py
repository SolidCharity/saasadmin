from rest_framework import serializers

from apps.backend.models import SaaSInstance

class SaaSInstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SaaSInstance
        fields = ('id', 'hostname', 'status')
