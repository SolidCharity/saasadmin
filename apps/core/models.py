from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class SaasCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    newsletter = models.BooleanField(_("newsletter"), default=True)
    newsletter_subscribed_on = models.DateTimeField(_("newsletter_subscribed_on"), null=True)
    newsletter_cancelled = models.DateTimeField(_("newsletter_cancelled"), null=True)
    language_code = models.CharField(_("language_code"), max_length=16, default="de")
    verified = models.BooleanField(_("verified"), default=True)
    verification_token = models.CharField(_("verification_token"), max_length=64, null=True)
    verification_until = models.DateTimeField(_("verification_until"), null=True)
    organisation_name = models.CharField(_("organisation_name"), max_length=64, null=True)
    first_name = models.CharField(_("first_name"), max_length=64, null=True)
    last_name = models.CharField(_("last_name"), max_length=64, null=True)
    street = models.CharField(_("street"), max_length=64, null=True)
    number = models.CharField(_("number"), max_length=11, null=True)
    post_code = models.CharField(_("post_code"), max_length=10, null=True)
    city = models.CharField(_("city"), max_length=16, null=True)
    country_code = models.CharField(_("country_code"), max_length=16, default="DE")
    email_address = models.EmailField(_("email_address"))
    is_active = models.BooleanField(_("ist_active"), default=True)

    class Meta:
        db_table = "saas_customer"

class SaasProduct (models.Model):
    name = models.CharField(_("name"), max_length=16)
    activationurl = (models.CharField(_("activationurl"), max_length=200))

    class Meta:
        db_table = "saas_product"

class SaasProductLanguage (models.Model):
    product = models.ForeignKey(
        SaasProduct,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )
    language = (models.CharField(_("language"), max_length=10, default = "DE"))
    payment_details = (models.CharField(_("payment_details"), max_length=300, default = ""))

    class Meta:
        db_table = "saas_product_language"

class SaasPlan (models.Model):
    name = models.CharField(_("name"), max_length=16)
    product = models.ForeignKey(
        SaasProduct,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )
    periodLengthInMonths = models.IntegerField(_("length"))
    currencyCode = models.CharField(_("currency"), max_length= 3, default= "EUR")
    costPerPeriod = models.DecimalField(_("cost"), max_digits= 10, decimal_places= 2)
    noticePeriodTypeInDays = models.IntegerField(_("notice"))
    language = (models.CharField(_("language"), max_length=10, default = "DE"))
    descr_target = (models.CharField(_("descr_target"), max_length=200, default = "TODO"))
    descr_caption = (models.CharField(_("descr_caption"), max_length=200, default = "TODO"))
    descr_1 = (models.CharField(_("descr_1"), max_length=200, default = "TODO"))
    descr_2 = (models.CharField(_("descr_2"), max_length=200, default = "TODO"))
    descr_3 = (models.CharField(_("descr_3"), max_length=200, default = "TODO"))
    descr_4 = (models.CharField(_("descr_4"), max_length=200, default = "TODO"))

    class Meta:
        db_table = "saas_plan"

# this is the saas instance rented by the customer
class SaasInstance(models.Model):
    identifier = models.CharField(_("identifier"), max_length=16, unique=True)

    product = models.ForeignKey(
        SaasProduct,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    hostname = models.CharField(_("hostname"), max_length=128, default='localhost')
    port = models.IntegerField(_("port"), default=-1)
    status = models.CharField(_("Status"), max_length=16, default='in_preparation')
    auto_renew = models.BooleanField(_("Auto Renew"), default=True)
    db_password = models.CharField(_("DB Password"), max_length=64, default='topsecret')
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


