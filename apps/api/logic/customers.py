from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail, mail_admins
from django.db import transaction
from django.utils import translation
from django.utils.translation import gettext as _
from apps.core.models import SaasContract, SaasCustomer, SaasInstance, SaasPlan
from apps.api.logic.instances import LogicInstances

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
            # send message to administrator
            self.notify_administrators(_("Missing free instance for %s") % (product.name,), _("Assigning of %s instance for customer %d failed") % (product.name, customer.id))

            # TODO if no instance is available, then add the user to the waiting list

            return False
        else:
            # assign a free instance
            # TODO: do we have already a contract?
            contract = self.get_new_contract(customer, product, plan)
            contract.instance = instance
            contract.is_confirmed = True
            contract.save()
            instance.status = 'assigned'
            instance.save()

            # call activation url of hosted application
            [success, PasswordResetToken] = LogicInstances().activate_instance(customer, product, instance)

            if not success:
                # send message to administrator
                self.notify_administrators(_("SaasAdmin Error during activation"), _("Failed activation of %s instance %s for customer %d") % (product.name, instance.identifier, customer.id))
                return False

            # TODO send notification email to customer, with password reset token
            # self.notify_customer(customer, _(""))

            # send message to administrator
            self.notify_administrators(_("Instance for %s assigned") % (product.name,), _("Nice, an instance of %s was booked for customer %d") % (product.name, customer.id))

            # TODO send invoice to customer, or send it later in batch processing?
            return True


    def notify_customer(self, customer, subject, message):
        send_mail(
            subject,
            message,
            None,
            [customer.email_address],
            fail_silently=False,
        )


    def notify_administrators(self, subject, message):
        mail_admins(
            subject,
            message,
            fail_silently=False,
        )


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
            print(contract.end_date)
            print(contract.latest_cancel_date)
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