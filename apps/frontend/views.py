from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import translation
from apps.api.logic.products import LogicProducts
from apps.core.models import SaasCustomer, SaasPlan
from apps.frontend.forms import CustomerForm
from apps.api.logic.customers import LogicCustomers
from apps.api.logic.plans import LogicPlans

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

    logic = LogicCustomers()
    product = LogicProducts().get_product(request);
    if product and not logic.has_instance(customer, product):
        if logic.assign_instance(customer, product):
            # TODO message to customer to inform about new instance
            None
        else:
            # TODO what about the situation where there is no free instance available
            None

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
    product = LogicProducts().get_product(request)
    plans = LogicPlans().get_plans(product)

    if plan_id == 'current':
        # TODO load current plan
        plan_id = plans.first().name
    else:
        # TODO store current plan (if it is a valid name)
        None
    return render(request, 'plan.html', {'product': product, 'plans': plans, 'selected_plan': plan_id})

@login_required
def select_payment(request):
    product = LogicProducts().get_product(request)
    return render(request, 'payment.html', {'product': product})

def display_pricing(request):
    product = LogicProducts().get_product(request)

    if product is None:
        products = LogicProducts().get_products()
        return render(request, 'select_product.html', {'products': products, 'hostname': request.META['HTTP_HOST']})

    plans = LogicPlans().get_plans(product)

    return render(request, 'pricing.html', {'product': product, 'plans': plans, 'popular_plan': plans[1].name})
