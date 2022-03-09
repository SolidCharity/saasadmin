from rest_framework import serializers

from apps.core.models import SaasInstance

class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    instance_url = serializers.SerializerMethodField('get_instance_url')

    def get_instance_url(self, instance):
      prod = instance.product
      return prod.instance_url.replace('%prefix', prod.instance_prefix).replace('%identifier', instance.identifier)

    class Meta:
        model = SaasInstance
        fields = ('identifier', 'hostname', 'pacuser', 'activation_token', 'db_password', 'initial_password', 'first_port', 'last_port', 'status', 'instance_url')
