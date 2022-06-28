from rest_framework import serializers
from apps.api.logic.contracts import LogicContracts

from apps.core.models import SaasInstance

class InstanceSerializer(serializers.HyperlinkedModelSerializer):
    instance_url = serializers.SerializerMethodField('get_instance_url')
    prefix = serializers.SerializerMethodField('get_prefix')
    quota_storage = serializers.SerializerMethodField('get_quota_storage')
    quota_app = serializers.SerializerMethodField('get_quota_app')

    def get_instance_url(self, instance):
        return instance.get_url()

    def get_prefix(self, instance):
      return instance.product.prefix

    def get_quota_storage(self, instance):
      plan = LogicContracts().get_plan_of_instance(instance)
      if not plan:
          raise Exception('Missing plan for product')
      return plan.quota_storage

    def get_quota_app(self, instance):
      plan = LogicContracts().get_plan_of_instance(instance)
      if not plan:
          raise Exception('Missing plan for product')
      return plan.quota_app

    class Meta:
        model = SaasInstance
        fields = ('identifier', 'hostname', 'pacuser', 'activation_token', 'db_password', 'initial_password', 'first_port', 'last_port', 'status', 'instance_url', 'prefix', 'password1', 'password2', 'django_secret_key', 'quota_storage', 'quota_app', 'custom_domain')
