from django.core.mail import send_mail, mail_admins
from django.db import transaction
from django.utils import translation
from django.utils.translation import gettext as _
from apps.core.models import SaasContract, SaasCustomer, SaasInstance, SaasPlan
from apps.api.logic.instances import LogicInstances
from apps.api.logic.contracts import LogicContracts

class LogicCustomers:

    @transaction.atomic
    def assign_instance(self, customer, product, plan, additional_storage):

        # check for first available instance
        instance = SaasInstance.objects.filter(product=product).filter(status=SaasInstance().AVAILABLE).first()
        if not instance:
            # send message to administrator
            self.notify_administrators(_("Missing free instance for %s") % (product.name,), _("Assigning of %s instance for customer %d failed") % (product.name, customer.id))

            # TODO if no instance is available, then add the user to the waiting list

            return False
        else:
            # assign a free instance
            # there might be an unconfirmed contract already
            contract = LogicContracts().get_contract(customer, product)
            if not contract:
                contract = LogicContracts().get_new_contract(customer, product, plan, 0)
            contract.instance = instance
            contract.plan = plan
            contract.is_confirmed = True

            # if payment is via direct debit but the sepa mandate has not been set yet
            if contract.payment_method == "SEPA_DIRECTDEBIT":
                if not contract.sepa_mandate:
                    contract.sepa_mandate = f"{contract.instance.identifier}{contract.sepa_mandate_date:%Y%m%d}"

            contract.save()
            instance.status = instance.ASSIGNED
            if additional_storage:
                instance.additional_storage = additional_storage
            instance.save()

            # call activation url of hosted application
            [success, PasswordResetToken] = LogicInstances().activate_instance(customer, product, instance)

            if not success:
                ExceptionMessage = PasswordResetToken
                # send message to administrator
                self.notify_administrators(_("SaasAdmin Error during activation"), _("Failed activation of %s instance %s for customer %d Exception: %s") % (product.name, instance.identifier, customer.id, ExceptionMessage))
                return False

            # send message to administrator
            instances_available = LogicInstances().get_number_of_available_instances(product)
            self.notify_administrators(_("Instance for %s assigned") % (product.name,),
                _("Nice, an instance of %s was booked for customer %d") % (product.name, customer.id) + "\n" +
                _("Still %d instances are available for new customers.") % (instances_available,))

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
