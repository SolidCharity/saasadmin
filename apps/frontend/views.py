from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from apps.core.models import SaasCustomer
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
    form = CustomerForm(values, instance = customer)
    if form.is_valid():
        form.save()
        return render(request, 'account.html', {'customer': customer, 'form': form, 'lang': lang})
    return render(request, 'account.html', {'customer': customer, 'form': form, 'lang': lang})

@login_required
def select_plan(request):
    return render(request, 'product.html', {})

@login_required
def select_payment(request):
    return render(request, 'payment.html', {})

def display_pricing(request):
    return render(request, 'pricing.html', {})
