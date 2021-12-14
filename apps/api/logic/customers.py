from django.utils import translation
from apps.core.models import SaasCustomer, SaasPlan

class LogicCustomers:

    def has_instance(self, customer):
        # TODO
        None

    def assign_instance(self, customer):
        # TODO if no instance is available, then add the user to the waiting list; send notification email to admin; return False
        # TODO assign a free instance
        # TODO call openpetra api SetInitialSysadminEmail
        # TODO send notification email to admin
        None