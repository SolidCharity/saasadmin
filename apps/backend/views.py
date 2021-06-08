from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.core.models import SaasInstance
from apps.core.models import SaasCustomer
from apps.core.models import SaasPlan
from apps.backend.forms import PlanForm
from django.db.models import Q
from django.db import connection
import sqlite3




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
    unused_instances = SaasInstance.objects.filter(Q(status='free') | Q(status='in_preparation'))
    plans = SaasPlan.objects.all()
    customers = SaasCustomer.objects.all()
    with connection.cursor() as cursor:
        connection.row_factory = sqlite3.Row

        sql = """SELECT email_address, person_name, instance.id as instance_id  
            FROM customer , instance, contract 
            WHERE contract.customer_id = customer.id 
            AND contract.instance_id = instance.id"""

        cursor.execute(sql)
        customers = cursor.fetchall()

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

@login_required
def editplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    form = PlanForm(request.POST or None, instance = plan)
    return render(request,'editplan.html', {'plan':plan, 'form': form})

@login_required
def updateplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    form = PlanForm(values, instance = plan)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'editplan.html', {'plan': plan, 'form': form})

@login_required
def deleteplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    plan.delete()
    return redirect("/")