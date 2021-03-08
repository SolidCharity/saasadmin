from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# this is the saas instance rented by the customer
class SaaSInstance(models.Model):
    hostname = models.CharField(_("hostname"), max_length=128, default='localhost')
    status = models.CharField(_("Status"), max_length=16, default='free')
    auto_renew = models.BooleanField(_("Auto Renew"), default=True)
    last_interaction = models.DateTimeField(_("Last Interaction"))
    reserved_token = models.CharField(max_length=64)
    reserved_until = models.DateTimeField(_("Reserved Until"))
    reserved_for_user = models.ForeignKey(
        User,
        null=True, blank=True, default = None,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_list",
    )

    class Meta:
        db_table = "instance"
