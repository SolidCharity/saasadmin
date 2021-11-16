from django import forms  
import sys
import datetime
from apps.core.models import SaasCustomer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = SaasCustomer
        fields = ("first_name", "last_name", "street", "post_code", "city", "country_code")

