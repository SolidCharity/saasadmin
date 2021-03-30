from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# this is the saas instance rented by the customer
class SaasInstance(models.Model):
    identifier = models.CharField(_("identifier"), max_length=16)
    hostname = models.CharField(_("hostname"), max_length=128, default='localhost')
    status = models.CharField(_("Status"), max_length=16, default='free')
    auto_renew = models.BooleanField(_("Auto Renew"), default=True)
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
        db_table = "instance"


class SaasPlan (models.Model):
    name = models.CharField(_("name"), max_length=16)
    periodLengthInMonths = models.IntegerField(_("length"))
    currencyCode = models.CharField(_("currency"), max_length= 3, default= "EUR")
    costPerPeriod = models.DecimalField(_("cost"), max_digits= 10, decimal_places= 2)
    noticePeriodTypeInDays = models.IntegerField(_("notice"))

    class Meta:
        db_table = "plan"
