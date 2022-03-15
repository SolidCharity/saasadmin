from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.utils import translation
from django.db import transaction
from apps.core.models import SaasContract, SaasCustomer, SaasInstance, SaasPlan

class LogicCustomers:

    def has_contract(self, customer, product):
        plans = SaasPlan.objects.filter(product=product).all()
        return SaasContract.objects.filter(customer=customer).filter(plan__in=plans).count() > 0

    def get_contract(self, customer, product):
        plans = SaasPlan.objects.filter(product=product).all()
        return SaasContract.objects.filter(customer=customer).filter(plan__in=plans).order_by('start_date').last()

    @transaction.atomic
    def assign_instance(self, customer, product, plan):
        # check for first available instance
        instance = SaasInstance.objects.filter(product=product).filter(status='free').first()
        if not instance:
            # TODO if no instance is available, then add the user to the waiting list; send notification email to admin; return False
            return False
        else:
            # assign a free instance
            contract = self.get_new_contract(customer, product, plan)
            contract.instance = instance
            contract.save()
            instance.status = 'assigned'
            instance.save()

            # TODO call activation url of hosted application
            # TODO send notification email to admin
            # TODO send notification email to customer
            # TODO send invoice to customer
            return True


    def get_new_contract(self, customer, product, plan):
        contract = SaasContract()
        contract.customer = customer
        contract.instance = None
        contract.plan = plan
        contract.auto_renew = True

        contract.start_date = datetime.today()
        nextMonthFirstDay = (contract.start_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        contract.end_date = nextMonthFirstDay + relativedelta(months=plan.periodLengthInMonths) - timedelta(days=1)
        contract.latest_cancel_date = contract.end_date - timedelta(days=plan.noticePeriodInDays)

        return contract


    # TODO: modify_contract