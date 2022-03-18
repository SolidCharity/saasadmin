from django.core.mail import send_mail, mail_admins
from django.db import transaction
from django.utils import translation
from django.utils.translation import gettext as _
from apps.core.models import SaasContract, SaasCustomer, SaasInstance, SaasPlan
from apps.api.logic.instances import LogicInstances
from apps.api.logic.contracts import LogicContracts

class LogicCustomers:

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
            contract = LogicContracts().get_new_contract(customer, product, plan)
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
