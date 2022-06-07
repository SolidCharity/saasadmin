from django import forms
from django.utils.translation import gettext_lazy as _
import datetime
from apps.core.models import SaasPlan, SaasProduct, SaasConfiguration, SaasInstance


class PlanForm(forms.ModelForm):

    class Meta:
        model = SaasPlan
        fields = ("slug", "name", "is_public", "priority", "is_favourite", "period_length_in_months", "period_length_in_days", "cost_per_period", "currency_code", "notice_period_in_days", "quota_app", "quota_storage", "descr_target", "descr_caption", "descr_1", "descr_2", "descr_3", "descr_4")

class ProductForm(forms.ModelForm):

    upstream_url = forms.URLField(label=_("Upstream URL"))
    description = forms.CharField(widget=forms.Textarea, label=_("Description"))

    class Meta:
        model = SaasProduct
        fields = ("slug", "name", "prefix",
            "instance_url", "instance_password_reset_url",
            "instance_admin_user",
            "number_of_ports", "is_active", "description", "upstream_url", "login_url")


class AddInstancesForm(forms.Form):
    product_id = forms.IntegerField()
    hostname = forms.CharField(max_length=128)
    pacuser = forms.CharField(max_length=128)
    count = forms.IntegerField()

class ConfigurationForm(forms.ModelForm):
    value = forms.CharField(widget=forms.Textarea, label=_("Value"))

    class Meta:
        model = SaasConfiguration
        fields = ("name", "value")

class InstanceForm(forms.ModelForm):

    class Meta:
        model = SaasInstance
        fields = ("custom_domain",)


