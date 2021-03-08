from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.backend.models import SaaSInstance

def home(request):
    # if not logged in => redirect to login screen
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.user.is_staff:
        return backend(request)
    # if logged in customer => redirect frontend view
    return redirect('/monitor')

@login_required
def backend(request):
    unused_instances = SaaSInstance.objects.filter(status='free')
    customers = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)

    return render(request,"backend.html",
            {'unused_instances':unused_instances,
             'customers':customers})
