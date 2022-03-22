from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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

    def get_contract(self, customer, product):
        plans = SaasPlan.objects.filter(product=product).all()
        return SaasContract.objects.filter(customer=customer).filter(plan__in=plans).order_by('start_date').last()

    def get_new_contract(self, customer, product, plan):
        contract = SaasContract()
        contract.customer = customer
        contract.instance = None
        contract.plan = plan

        contract.start_date = datetime.today()
        if plan.period_length_in_months == 0:
            contract.end_date = contract.start_date + timedelta(days=1)
            contract.latest_cancel_date = None
            contract.is_auto_renew = False
        else:
            nextMonthFirstDay = (contract.start_date.replace(day=1) + timedelta(days=32)).replace(day=1)
            contract.end_date = nextMonthFirstDay + relativedelta(months=plan.period_length_in_months) - timedelta(days=1)
            contract.latest_cancel_date = contract.end_date - timedelta(days=plan.notice_period_in_days)
            contract.is_auto_renew = True

        contract.is_confirmed = False

        return contract


    def modify_contract(self, customer, product, plan):

        contract = self.get_contract(customer, product)

        # no change is necessary
        if contract.plan == plan:
            return contract

        new_contract = self.get_new_contract(customer, product, plan)
        contract.plan = new_contract.plan
        contract.start_date = new_contract.start_date
        contract.end_date = new_contract.end_date
        contract.latest_cancel_date = new_contract.latest_cancel_date
        contract.is_auto_renew = new_contract.is_auto_renew

        return contract

    # to be called by a cronjob each night
    def update_dates_of_contracts(self):
        contracts = SaasContract.objects.filter(is_confirmed = True, is_auto_renew = True, latest_cancel_date__lt = datetime.today())
        for contract in contracts:
            temp_contract = self.get_new_contract(contract.customer, contract.instance.product, contract.plan)
            contract.end_date = temp_contract.end_date
            contract.latest_cancel_date = temp_contract.latest_cancel_date
            contract.save()
