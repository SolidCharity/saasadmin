from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    instances = SaaSInstance.objects.filter(status='free')

    return render(request,"backend.html",
            {'instances':instances})
