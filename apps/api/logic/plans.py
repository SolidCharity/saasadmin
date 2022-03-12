from django.utils import translation
from apps.core.models import SaasCustomer, SaasPlan
from django.conf import settings

class LogicPlans:

    def get_plans(self, product):
        cur_language = translation.get_language().upper()
        if cur_language not in settings.AVAILABLE_FRONTEND_LANGUAGES:
            cur_language = settings.DEFAULT_FRONTEND_LANGUAGE

        plans = SaasPlan.objects.filter(language=cur_language, product=product).order_by('costPerPeriod')
        if plans.count() == 0:
            plans = SaasPlan.objects.filter(language=settings.DEFAULT_FRONTEND_LANGUAGE, product=product).order_by('costPerPeriod')

        return plans

    def get_plan(self, product, plan_id):
        plans = self.get_plans(product)
        return plans.filter(name=plan_id).first()
