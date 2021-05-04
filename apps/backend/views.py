from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.core.models import SaasInstance
from apps.core.models import SaasPlan
from apps.backend.forms import PlanForm




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
    unused_instances = SaasInstance.objects.filter(status='free')
    plans = SaasPlan.objects.all()
    customers = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
    # addplan = user.objects.

    return render(request,"backend.html",
            {'unused_instances':unused_instances,
             'plans':plans,
             'customers':customers})

@login_required
def addplan(request):


    if request.method == "POST":
        # request.POST is immutable, so make a copy
        values = request.POST.copy()
        values['owner'] = request.user.id
        form = PlanForm(values)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = PlanForm()
    return render(request,'addplan.html',{'form':form})