from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from simple_history.models import HistoricalRecords

class SaasConfiguration(models.Model):
    name = models.CharField(_("name"), max_length=64)
    value = models.CharField(_("value"), max_length=5000)

    class Meta:
        db_table = "saas_configuration"

class SaasCustomer(models.Model):
    history = HistoricalRecords()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_newsletter_subscribed = models.BooleanField(_("Subscribed to newsletter"), default=False)
    newsletter_subscribed_on = models.DateTimeField(_("newsletter_subscribed_on"), null=True)
    newsletter_cancelled = models.DateTimeField(_("newsletter_cancelled"), null=True)
    language_code = models.CharField(_("language_code"), max_length=16, default="de")
    organisation_name = models.CharField(_("organisation_name"), max_length=64, null=True, blank=True)

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

    def get_name(self):
        if self.organisation_name:
            return self.organisation_name
        return self.last_name + " " + self.first_name

class SaasProduct (models.Model):
    slug = models.CharField(_("Slug"), max_length=50, default = "invalid", unique=True)
    name = models.CharField(_("Name"), max_length=16)
    prefix = models.CharField(_("Prefix"), max_length=10, default='xy')
    activation_url = models.CharField(_("Activation URL"), max_length=250, default = "")
    deactivation_url = models.CharField(_("Deactivation URL"), max_length=250, default = "")
    instance_url = models.CharField(_("Instance URL"), max_length=250, default = "https://#Prefix#Identifier.example.org/")
    instance_password_reset_url = models.CharField(_("Password Reset URL"), max_length=250, default = "/reset_password")
    instance_admin_user = models.CharField(_("Instance Admin User"), max_length=100, default = "admin")
    is_active = models.BooleanField(_("Is Active"), default=False)
    number_of_ports = models.IntegerField(_("Number of Ports"), default=1)
    # 2 sentences
    description = models.CharField(_("Description"), max_length=250, default="")
    # 5 sentences
    first_page_purpose = models.CharField(_("First Page Purpose"), max_length=1500, default="")
    # see https://djangocentral.com/uploading-images-with-django/
    first_page_logo = models.ImageField(_("First Page Logo"), upload_to='product_logos', null=True)

    upstream_url = models.CharField(_("Upstream_URL"), max_length=250, default = "https://example.org")
    login_url = models.CharField(_("Login_URL"), max_length=250, default = "/")

    POSTGRESQL, MYSQL = ('postgresql', 'mysql')
    DBMS_CHOICES = (
        (POSTGRESQL, _("PostgreSQL")),
        (MYSQL, _("MySQL/MariaDB")),
    )
    dbms_type = models.CharField(
        _("Database Type"),
        max_length=64, choices=DBMS_CHOICES, blank=False, default=MYSQL)

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
    priority = models.IntegerField(_("Sorting Order"), default = 0)
    is_favourite = models.BooleanField(_("is favourite"), default=False)
    is_public = models.BooleanField(_("is public"), default=True)
    # if period length in months is 0 and period length in days is 0, then this plan is unlimited, for free or one-time payment
    period_length_in_months = models.IntegerField(_("Period Length in Months"), default = 0)
    period_length_in_days = models.IntegerField(_("Period Length in Days"), default = 0)
    currency_code = models.CharField(_("Currency"), max_length= 3, default= "EUR")
    cost_per_period = models.DecimalField(_("Cost per Period"), max_digits= 10, decimal_places= 2)
    notice_period_in_days = models.IntegerField(_("Notice Period in Days"))
    descr_target = models.CharField(_("Description Target"), max_length=200, default = "TODO")
    descr_caption = models.CharField(_("Description Caption"), max_length=200, default = "TODO")
    descr_1 = models.CharField(_("Description 1"), max_length=200, default = "TODO")
    descr_2 = models.CharField(_("Description 2"), max_length=200, default = "TODO")
    descr_3 = models.CharField(_("Description 3"), max_length=200, default = "TODO")
    descr_4 = models.CharField(_("Description 4"), max_length=200, default = "TODO")
    quota_storage = models.CharField(_("Quota for Storage"), max_length=20, default = "0M")
    quota_app = models.CharField(_("Quota for Application"), max_length=20, default = "500M")
    cost_for_storage = models.DecimalField(_("Cost for Storage"), max_digits=10, decimal_places= 2, default=0)
    additional_storage_size = models.CharField(_("Additional Storage Size"), max_length=10, default = "")

    class Meta:
        db_table = "saas_plan"


    def get_included_storage_gb(self):
        if not self.quota_storage or self.quota_storage == '0M':
            return 0
        if not self.quota_storage.endswith("G"):
            raise Exception(f"Expected trailing G for quota storage in plan {self.name}, got {self.quota_storage}")
        return int(self.quota_storage.replace("G",""))


    def get_additional_storage_gb(self):
        if not self.additional_storage_size or self.additional_storage_size == '0M':
            return 0
        if not self.additional_storage_size.endswith("G"):
            raise Exception(f"Expected trailing G for additional storage size in plan {self.name}, got {self.additional_storage_size}")
        return int(self.additional_storage_size.replace("G",""))

# this is the saas instance rented by the customer
class SaasInstance(models.Model):
    history = HistoricalRecords()

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
    custom_domain = models.CharField(_("Custom Domain"),max_length=250, default = "", null=True, blank=True)
    additional_storage = models.IntegerField(_("Additional Storage"), default = 0)

    # possible values for status
    IN_PREPARATION, READY, AVAILABLE, RESERVED, ASSIGNED, EXPIRED, TO_BE_REMOVED, REMOVED = \
        ('IN_PREPARATION', 'READY', 'AVAILABLE', 'RESERVED', 'ASSIGNED', 'EXPIRED', 'TO_BE_REMOVED', 'REMOVED')
    status = models.CharField(_("Status"), max_length=16, default='in_preparation')

    db_password = models.CharField(_("DB Password"), max_length=64, default='topsecret')
    initial_password = models.CharField(_("Initial Password"), max_length=64, default='topsecret')
    # for example nextcloud: redis password
    password1 = models.CharField(_("Password1"), max_length=64, default='topsecret')
    # for example nextcloud: turn server password
    password2 = models.CharField(_("Password2"), max_length=64, default='topsecret')
    # for django installations
    django_secret_key = models.CharField(_("Django Secret Key"), max_length=64, default='topsecret')
    last_interaction = models.DateTimeField(_("Last Interaction"), null=True)
    reserved_token = models.CharField(_("Reserved Token"), max_length=64, null=True)
    reserved_until = models.DateTimeField(_("Reserved Until"), null=True)
    reserved_for_user = models.ForeignKey(
        User,
        null=True, blank=True, default = None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    POSTGRESQL, MYSQL = ('postgresql', 'mysql')
    DBMS_CHOICES = (
        (POSTGRESQL, _("PostgreSQL")),
        (MYSQL, _("MySQL/MariaDB")),
    )
    dbms_type = models.CharField(
        _("Database Type"),
        max_length=64, choices=DBMS_CHOICES, blank=False, default=MYSQL)

    class Meta:
        db_table = "saas_instance"
        constraints = [
            models.UniqueConstraint(fields=['identifier', 'product'], name='identifier and product')
        ]

    def get_url(self, custom_domain=True):
        if self.custom_domain and custom_domain:
            return f"https://{self.custom_domain}"
        else:
            prod = self.product
            return prod.instance_url.replace('#Prefix', prod.prefix).replace('#Identifier', self.identifier)


class SaasContract(models.Model):

    history = HistoricalRecords(
        # to avoid error: HistoricalSaasContract() got an unexpected keyword argument 'instance_id'
        excluded_fields={"instance"}
    )

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
