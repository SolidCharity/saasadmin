from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class SaasConfiguration(models.Model):
    name = models.CharField(_("name"), max_length=64)
    language = models.CharField(_("language"), max_length=10)
    value = models.CharField(_("value"), max_length=250)

    class Meta:
        db_table = "saas_configuration"

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

    MR, MRS, MRDR, MRSDR = ('Mr', 'Mrs', 'Mr Dr', 'Mrs Dr')
    TITLE_CHOICES = (
        (MR, _("Mr")),
        (MRS, _("Mrs")),
        (MRDR, _("Mr Dr")),
        (MRSDR, _("Mrs Dr")),
    )
    title = models.CharField(
        _("Title"),
        max_length=64, choices=TITLE_CHOICES, blank=True)

    first_name = models.CharField(_("first_name"), max_length=64, default='')
    last_name = models.CharField(_("last_name"), max_length=64, default='')
    street = models.CharField(_("street"), max_length=64, default='')
    post_code = models.CharField(_("post_code"), max_length=10, default='')
    city = models.CharField(_("city"), max_length=16, default='')
    country_code = CountryField(_("country"), default='DE')
    email_address = models.EmailField(_("email_address"))
    is_active = models.BooleanField(_("is_active"), default=True)

    class Meta:
        db_table = "saas_customer"

class SaasProduct (models.Model):
    slug = models.CharField(_("slug"), max_length=50, default = "invalid", unique=True)
    name = models.CharField(_("name"), max_length=16)
    activation_url = models.CharField(_("Activation URL"), max_length=250, default = "https://%prefix%identifier.example.org/activate")
    instance_url = models.CharField(_("Instance URL"), max_length=250, default = "https://%prefix%identifier.example.org")
    is_active = models.BooleanField(_("is active"), default=False)
    number_of_ports = models.IntegerField(_("number of ports"), default=1)
    instance_prefix = models.CharField(_("instance prefix"), max_length=10, default='xy')

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
    period_length_in_months = models.IntegerField(_("Period Length in Months"))
    currency_code = models.CharField(_("currency"), max_length= 3, default= "EUR")
    cost_per_period = models.DecimalField(_("Cost per Period"), max_digits= 10, decimal_places= 2)
    notice_period_in_days = models.IntegerField(_("Notice Period in Days"))
    language = (models.CharField(_("Language"), max_length=10, default = "DE"))
    descr_target = (models.CharField(_("Description Target"), max_length=200, default = "TODO"))
    descr_caption = (models.CharField(_("Description Caption"), max_length=200, default = "TODO"))
    descr_1 = (models.CharField(_("Description 1"), max_length=200, default = "TODO"))
    descr_2 = (models.CharField(_("Description 2"), max_length=200, default = "TODO"))
    descr_3 = (models.CharField(_("Description 3"), max_length=200, default = "TODO"))
    descr_4 = (models.CharField(_("Description 4"), max_length=200, default = "TODO"))

    class Meta:
        db_table = "saas_plan"

# this is the saas instance rented by the customer
class SaasInstance(models.Model):
    identifier = models.CharField(_("identifier"), max_length=16)

    product = models.ForeignKey(
        SaasProduct,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    hostname = models.CharField(_("hostname"), max_length=128, default='localhost')
    pacuser = models.CharField(_("pacuser"), max_length=128, default='xyz00')
    channel = models.CharField(_("channel"), max_length=128, default='stable')
    first_port = models.IntegerField(_("first port"), default=-1)
    last_port = models.IntegerField(_("last port"), default=-1)
    activation_token = models.CharField(max_length=64, null=True)

    # possible values: in_preparation, new, active, expired, cancelled, to_be_removed, deleted
    status = models.CharField(_("Status"), max_length=16, default='in_preparation')
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
        constraints = [
            models.UniqueConstraint(fields=['identifier', 'product'], name='identifier and product')
        ]

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

    start_date = models.DateField(_("start_date"), null=True )
    end_date = models.DateField(_("end_date"), null=True)
    latest_cancel_date = models.DateField(_("latest_cancel_date"), null=True)
    auto_renew = models.BooleanField(_("auto_renew"), default= True)

    class Meta:
        db_table = "saas_contract"
