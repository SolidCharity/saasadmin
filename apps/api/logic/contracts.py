from django.utils import translation
from apps.core.models import SaasContract, SaasPlan, SaasCustomer
from django.db.models import Q
from datetime import date

class LogicContracts:

    def get_current_plan(self, request, product):
        customer = SaasCustomer.objects.filter(user=request.user).first()
        plans = SaasPlan.objects.filter(product=product).all()
        contracts = SaasContract.objects.filter(customer=customer).filter(plan__in=plans).filter(Q(end_date__isnull=True)|Q(end_date__gt=date.today()))
        if contracts.first():
            return contracts.first().plan
        return None