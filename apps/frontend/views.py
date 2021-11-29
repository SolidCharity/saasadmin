from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from apps.core.models import SaasCustomer, SaasPlan
from apps.frontend.forms import CustomerForm

def home(request):
    # if not logged in => redirect to pricing
    if not request.user.is_authenticated:
        return redirect('/pricing')
    if request.user.is_staff:
        return redirect('/backend')
    # if logged in customer => redirect frontend view
    return redirect('/account')

@login_required
def account_view(request):
    lang="en"
    customer = SaasCustomer.objects.filter(user=request.user).first()
    if customer is None:
        # create a new customer for this user
        customer = SaasCustomer()
        customer.user = request.user
        customer.email_address = request.user.email
        customer.save()

    return render(request, 'account.html', {'customer': customer, 'lang': lang})

@login_required
def account_update(request):
    lang="en"

    customer = SaasCustomer.objects.filter(user=request.user).first()
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    values['user'] = request.user.id

    form = CustomerForm(values, instance = customer)
    if form.is_valid():
        form.save()
        return redirect('/account')
    return render(request, 'account.html', {'customer': customer, 'form': form, 'lang': lang})

@login_required
def select_plan(request, plan_id):
    plans = SaasPlan.objects.filter(language="de").order_by('costPerPeriod')
    if plan_id == 'current':
        # load current plan
        plan_id = plans.first().name
    else:
        # TODO store current plan
        None
    return render(request, 'plan.html', {'plans': plans, 'selected_plan': plan_id})

@login_required
def select_payment(request):
    return render(request, 'payment.html', {})

def display_pricing(request):
    plans = SaasPlan.objects.filter(language="de").order_by('costPerPeriod')
    return render(request, 'pricing.html', {'plans': plans, 'popular_plan': 'Basic'})
