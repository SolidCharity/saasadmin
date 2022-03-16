from django.utils import translation
from apps.core.models import SaasCustomer, SaasPlan
from django.conf import settings

class LogicPlans:

    def get_plans(self, product):
        return SaasPlan.objects.filter(product=product).order_by('cost_per_period')

    def get_plan(self, product, plan_id):
        plans = self.get_plans(product)
        return plans.filter(name=plan_id).first()
