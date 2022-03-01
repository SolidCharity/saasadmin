from django import forms
import datetime
from apps.core.models import SaasPlan, SaasProduct


class PlanForm(forms.ModelForm):

    class Meta:
        model = SaasPlan
        fields = ("name", "periodLengthInMonths", "costPerPeriod", "currencyCode", "noticePeriodTypeInDays", "language", "descr_target", "descr_caption", "descr_1", "descr_2", "descr_3", "descr_4")


class ProductForm(forms.ModelForm):

    class Meta:
        model = SaasProduct
        fields = "__all__"


class AddInstancesForm(forms.Form):
    product_id = forms.IntegerField()
    hostname = forms.CharField(max_length=128)
    count = forms.IntegerField()