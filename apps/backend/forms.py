from django import forms
import datetime
from apps.core.models import SaasPlan


class PlanForm(forms.ModelForm):

    class Meta:
        model = SaasPlan
        fields = "__all__"


from django import forms
import datetime
from apps.core.models import SaasProduct


class ProductForm(forms.ModelForm):

    class Meta:
        model = SaasProduct
        fields = "__all__"