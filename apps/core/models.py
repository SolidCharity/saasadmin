from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

class SaasConfiguration(models.Model):
    name = models.CharField(_("name"), max_length=64)
    value = models.CharField(_("value"), max_length=250)

    class Meta:
        db_table = "saas_configuration"

class SaasCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_newsletter_subscribed = models.BooleanField(_("Subscribed to newsletter"), default=False)
    newsletter_subscribed_on = models.DateTimeField(_("newsletter_subscribed_on"), null=True)
    newsletter_cancelled = models.DateTimeField(_("newsletter_cancelled"), null=True)
    language_code = models.CharField(_("language_code"), max_length=16, default="de")
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

    first_name = models.CharField(_("First Name"), max_length=64, default='')
    last_name = models.CharField(_("Last Name"), max_length=64, default='')
    street = models.CharField(_("Street and housenumber"), max_length=64, default='')
    post_code = models.CharField(_("Post Code"), max_length=10, default='')
    city = models.CharField(_("City"), max_length=16, default='')
    country_code = CountryField(_("Country"), default='DE')
    email_address = models.EmailField(_("Email Address"))
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        db_table = "saas_customer"

class SaasProduct (models.Model):
    slug = models.CharField(_("Slug"), max_length=50, default = "invalid", unique=True)
    name = models.CharField(_("Name"), max_length=16)
    prefix = models.CharField(_("Prefix"), max_length=10, default='xy')
    activation_url = models.CharField(_("Activation URL"), max_length=250, default = "https://%prefix%identifier.example.org/activate")
    deactivation_url = models.CharField(_("Deactivation URL"), max_length=250, default = "https://%prefix%identifier.example.org/deactivate")
    instance_url = models.CharField(_("Instance URL"), max_length=250, default = "https://%prefix%identifier.example.org")
    instance_password_reset_url = models.CharField(_("Password Reset URL"), max_length=250, default = "https://%prefix%identifier.example.org/reset_password?token=#PasswordResetToken")
    instance_admin_user = models.CharField(_("Instance Admin User"), max_length=100, default = "admin")
    is_active = models.BooleanField(_("Is Active"), default=False)
    number_of_ports = models.IntegerField(_("Number of Ports"), default=1)

    class Meta:
        db_table = "saas_product"

class SaasPlan (models.Model):
    slug = models.CharField(_("slug"), max_length=16)
    name = models.CharField(_("name"), max_length=16)
    product = models.ForeignKey(
        SaasProduct,
        null=False, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )
    is_favourite = models.BooleanField(_("is favourite"), default=False)
    period_length_in_months = models.IntegerField(_("Period Length in Months"))
    currency_code = models.CharField(_("Currency"), max_length= 3, default= "EUR")
    cost_per_period = models.DecimalField(_("Cost per Period"), max_digits= 10, decimal_places= 2)
    notice_period_in_days = models.IntegerField(_("Notice Period in Days"))
    descr_target = models.CharField(_("Description Target"), max_length=200, default = "TODO")
    descr_caption = models.CharField(_("Description Caption"), max_length=200, default = "TODO")
    descr_1 = models.CharField(_("Description 1"), max_length=200, default = "TODO")
    descr_2 = models.CharField(_("Description 2"), max_length=200, default = "TODO")
    descr_3 = models.CharField(_("Description 3"), max_length=200, default = "TODO")
    descr_4 = models.CharField(_("Description 4"), max_length=200, default = "TODO")

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

    hostname = models.CharField(_("Hostname"), max_length=128, default='localhost')
    pacuser = models.CharField(_("Packet User"), max_length=128, default='xyz00')
    channel = models.CharField(_("Channel"), max_length=128, default='stable')
    first_port = models.IntegerField(_("First Port"), default=-1)
    last_port = models.IntegerField(_("Last Port"), default=-1)
    activation_token = models.CharField(max_length=64, null=True)

    # possible values for status
    IN_PREPARATION, AVAILABLE, RESERVED, ASSIGNED, EXPIRED, TO_BE_REMOVED, REMOVED = \
        ('IN_PREPARATION', 'AVAILABLE', 'RESERVED', 'ASSIGNED', 'EXPIRED', 'TO_BE_REMOVED', 'REMOVED')
    status = models.CharField(_("Status"), max_length=16, default='in_preparation')

    db_password = models.CharField(_("DB Password"), max_length=64, default='topsecret')
    initial_password = models.CharField(_("Initial Password"), max_length=64, default='topsecret')
    last_interaction = models.DateTimeField(_("Last Interaction"), null=True)
    reserved_token = models.CharField(_("Reserved Token"), max_length=64, null=True)
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

    instance = models.ForeignKey(
        SaasInstance,
        null=True, blank=False, default=None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    start_date = models.DateField(_("Start Date"), null=True )
    end_date = models.DateField(_("End Date"), null=True)
    latest_cancel_date = models.DateField(_("Latest Cancel Date"), null=True)
    is_auto_renew = models.BooleanField(_("Is Renewing Automatically"), default=True)
    is_confirmed = models.BooleanField(_("Is Confirmed"), default=False)

    payment_method = models.CharField(_("Payment Method"), max_length=20, default="SEPA_TRANSFER") 
    account_owner = models.CharField(_("Account Owner"), max_length=200, null=True, default="")
    account_iban = models.CharField(_("Account IBAN"), max_length=64, null=True, default="")
    sepa_mandate = models.CharField(_("SEPA Mandate"), max_length=64, null=True, default="")
    sepa_mandate_date = models.DateField(_("Date of SEPA Mandate"), null=True)

    class Meta:
        db_table = "saas_contract"
