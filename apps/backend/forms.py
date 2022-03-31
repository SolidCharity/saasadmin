from django import forms
import datetime
from apps.core.models import SaasPlan, SaasProduct


class PlanForm(forms.ModelForm):

    class Meta:
        model = SaasPlan
        fields = ("slug", "name", "period_length_in_months", "cost_per_period", "currency_code", "notice_period_in_days", "descr_target", "descr_caption", "descr_1", "descr_2", "descr_3", "descr_4")


class ProductForm(forms.ModelForm):

    class Meta:
        model = SaasProduct
        fields = ("slug", "name", "prefix",
            "instance_url", "instance_password_reset_url",
            "instance_admin_user",
            "number_of_ports", "is_active")


class AddInstancesForm(forms.Form):
    product_id = forms.IntegerField()
    hostname = forms.CharField(max_length=128)
    pacuser = forms.CharField(max_length=128)
    count = forms.IntegerField()