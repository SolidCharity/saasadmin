from django import forms  
import sys
import datetime
from apps.core.models import SaasCustomer, SaasContract

class CustomerForm(forms.ModelForm):
    class Meta:
        model = SaasCustomer
        fields = ("email_address", "organisation_name", "title", "first_name", "last_name", "street", "post_code", "city", "country_code")

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['email_address'].disabled = True

