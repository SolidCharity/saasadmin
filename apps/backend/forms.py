from django import forms
import datetime
from apps.core.models import SaasPlan


class PlanForm(forms.ModelForm):

    class Meta:
        model = SaasPlan
        fields = "__all__"