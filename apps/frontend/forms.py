from django import forms  
import sys
import datetime
from apps.core.models import SaasCustomer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = SaasCustomer
        fields = "__all__"

