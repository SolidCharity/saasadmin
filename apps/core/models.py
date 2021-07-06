from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SaasCustomer(models.Model):
    newsletter = models.BooleanField(_("newsletter"), default=True)
    newsletter_subscribed_on = models.DateTimeField(_("newsletter_subscribed_on"), null=True)
    newsletter_cancelled = models.DateTimeField(_("newsletter_cancelled"), null=True)
    language_code = models.CharField(_("language_code"), max_length=16)
    verified = models.BooleanField(_("verified"), default=True)
    verification_token = models.CharField(_("verification_token"), max_length=64)
    verification_until = models.DateTimeField(_("verification_until"), null=True)
    organisation_name = models.CharField(_("organisation_name"), max_length=64)
    person_name = models.CharField(_("person_name"), max_length=64)
    street = models.CharField(_("street"), max_length=64)
    number = models.CharField(_("number"), max_length=11)
    post_code = models.CharField(_("post_code"), max_length=10)
    city = models.CharField(_("city"), max_length=16)
    country_code = models.CharField(_("country_code"), max_length=16)
    email_address = models.EmailField(_("email_address"))
    is_active = models.BooleanField(_("ist_active"), default=True)

    class Meta:
        db_table = "saas_customer"

# this is the saas instance rented by the customer
class SaasInstance(models.Model):
    identifier = models.CharField(_("identifier"), max_length=16, unique=True)
    hostname = models.CharField(_("hostname"), max_length=128, default='localhost')
    port = models.IntegerField(_("port"), default=-1)
    status = models.CharField(_("Status"), max_length=16, default='free')
    auto_renew = models.BooleanField(_("Auto Renew"), default=True)
    initial_password = models.CharField(_("Initial Password"), max_length=64, default='topsecret')
    last_interaction = models.DateTimeField(_("Last Interaction"), null=True)
    reserved_token = models.CharField(max_length=64, null=True)
    reserved_until = models.DateTimeField(_("Reserved Until"), null=True)
    reserved_for_user = models.ForeignKey(
        User,
        null=True, blank=True, default = None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    class Meta:
        db_table = "saas_instance"

class SaasPlan (models.Model):
    name = models.CharField(_("name"), max_length=16, unique=True)
    periodLengthInMonths = models.IntegerField(_("length"))
    currencyCode = models.CharField(_("currency"), max_length= 3, default= "EUR")
    costPerPeriod = models.DecimalField(_("cost"), max_digits= 10, decimal_places= 2)
    noticePeriodTypeInDays = models.IntegerField(_("notice"))

    class Meta:
        db_table = "saas_plan"

class SaasContract(models.Model):

    plan = models.ForeignKey(
        SaasPlan,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    customer = models.ForeignKey(
        SaasCustomer,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )
    #instance_id
    instance = models.ForeignKey(
        SaasInstance,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    start_date = models.DateTimeField(_("start_date"), null=True )
    end_date = models.DateTimeField(_("end_date"), null=True)
    auto_renew = models.BooleanField(_("auto_renew"), default= True)

    class Meta:
        db_table = "saas_contract"
