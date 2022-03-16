from django import forms  
import sys
import datetime
from apps.core.models import SaasCustomer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = SaasCustomer
        fields = ("email_address", "title", "first_name", "last_name", "street", "post_code", "city", "country_code")

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['email_address'].disabled = True

