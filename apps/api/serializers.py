from rest_framework import serializers

from apps.core.models import SaasInstance

class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SaasInstance
        fields = ('identifier', 'hostname', 'db_password', 'initial_password', 'port', 'status')
