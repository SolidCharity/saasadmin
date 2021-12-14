from django.utils import translation
from apps.core.models import SaasCustomer, SaasPlan

class LogicPlans:

    def get_plans(self):
        cur_language = translation.get_language()
        if "de" in cur_language:
            cur_language = "de"
        else:
            cur_language = "en"

        plans = SaasPlan.objects.filter(language=cur_language).order_by('costPerPeriod')
        if plans.count() == 0:
            plans = SaasPlan.objects.filter(language="de").order_by('costPerPeriod')

        return plans
