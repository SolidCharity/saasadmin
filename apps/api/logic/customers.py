from django.utils import translation
from apps.core.models import SaasContract, SaasCustomer, SaasInstance, SaasPlan
from datetime import datetime
from django.db import transaction

class LogicCustomers:

    def has_contract(self, customer, product):
        plans = SaasPlan.objects.filter(product=product).all()
        return SaasContract.objects.filter(customer=customer).filter(plan__in=plans).count() > 0

    def get_contract(self, customer, product):
        plans = SaasPlan.objects.filter(product=product).all()
        return SaasContract.objects.filter(customer=customer).filter(plan__in=plans).order_by('start_date').last()

    @transaction.atomic
    def assign_instance(self, customer, product):
        # check for first available instance
        instance = SaasInstance.objects.filter(product=product).filter(status='free').first()
        if not instance:
            # TODO if no instance is available, then add the user to the waiting list; send notification email to admin; return False
            return False
        else:
            # assign a free instance
            contract = SaasContract()
            contract.customer = customer
            contract.instance = instance
            contract.plan = SaasPlan.objects.filter(product=product).first()
            contract.start_date = datetime.now()
            contract.auto_renew = True
            contract.save()
            instance.status = 'assigned'
            instance.save()

            # TODO call openpetra api SetInitialSysadminEmail
            # TODO send notification email to admin
            # TODO send notification email to customer
            return True
