from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import translation
from django.utils.translation import gettext as _
from apps.api.logic.products import LogicProducts
from apps.core.models import SaasCustomer, SaasPlan, SaasProduct
from apps.frontend.forms import CustomerForm
from apps.api.logic.customers import LogicCustomers
from apps.api.logic.plans import LogicPlans
from apps.api.logic.contracts import LogicContracts

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

    form = CustomerForm(instance = customer)
    return render(request, 'account.html', {'customer': customer, 'form': form, 'lang': lang})

def  clean_null(customer):
    if customer.first_name is None:
        customer.first_name = ''
    if customer.last_name is None:
        customer.last_name = ''
    if customer.street is None:
        customer.street = ''
    if customer.post_code is None:
        customer.post_code = ''
    if customer.city is None:
        customer.city = ''

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
    current_plan = LogicContracts().get_current_plan(request, product)
    plans = LogicPlans().get_plans(product)

    # the customer has selected a plan
    if plan_id != 'current':
        # check if this is a valid plan
        new_plan = LogicPlans().get_plan(product, plan_id)
        return show_payment(request, product, current_plan, new_plan)

    # load booked plan from the database
    if current_plan:
        plan_id = current_plan.name
    else:
        plan_id = ''

    return render(request, 'plan.html', {'product': product, 'plans': plans, 'selected_plan': plan_id})

@login_required
def select_payment(request):
    product = LogicProducts().get_product(request)
    current_plan = LogicContracts().get_current_plan(request, product)
    if current_plan is None:
        return redirect('/plan/current')
    return show_payment(request, product, current_plan, None)


def readablePeriodsInMonths(periodLength):
    if periodLength == 12:
        return "1 " + _("year")
    elif periodLength == 1:
        return "1 " + _("month")
    else:
        return str(periodLength) + " " + _("months")

def readablePeriodsInDays(periodLength):
    if periodLength == 30:
        return "1 " + _("month")
    elif periodLength == 14:
        return "2 " + _("weeks")
    else:
        return str(periodLength) + " " + _("days")

def show_payment(request, product, current_plan, new_plan):
    if new_plan is None:
        new_plan = current_plan
    customer = SaasCustomer.objects.filter(user=request.user).first()
    contract = LogicCustomers().get_contract(customer, product)
    periodLength = readablePeriodsInMonths(new_plan.periodLengthInMonths)
    if new_plan.periodLengthInMonths == 1:
        periodLengthExtension = _("another month")
    elif new_plan.periodLengthInMonths == 3:
        periodLengthExtension = _("another quarter")
    elif new_plan.periodLengthInMonths == 12:
        periodLengthExtension = _("another year")
    isNewOrder = current_plan is None or current_plan.name != new_plan.name
    isNotNewContract = current_plan is not None and current_plan.name == new_plan.name
    noticePeriod = readablePeriodsInDays(new_plan.noticePeriodInDays)
    if not contract:
        # get new contract from logic
        contract = LogicCustomers().get_new_contract(customer, product, new_plan)

    return render(request, 'payment.html',
        {'product': product,
        'plan': new_plan,
        'contract': contract,
        'is_new_order': isNewOrder,
        'contract_exists': isNotNewContract,
        'noticePeriod': noticePeriod,
        'periodLength': periodLength,
        'periodLengthExtension': periodLengthExtension})


def subscribe(request, product_id, plan_id):
    logic = LogicCustomers()
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = SaasProduct.objects.filter(slug = product_id).first()
    if not product:
        raise Exception('invalid product')
    plan = LogicPlans().get_plan(product, plan_id)
    if not plan:
        raise Exception('invalid plan')

    if logic.has_contract(customer, product):
        # TODO upgrade or downgrade the plan?
        contract = logic.get_contract(customer, product)
        contract.plan = plan
        contract.save()

        # redirect to instance details page
        return redirect('/instance')

    else:
        # assign a new instance
        if logic.assign_instance(customer, product, plan):
            # redirect to instance details page
            return redirect('/instance')
        else:
            # TODO what about the situation where there is no free instance available
            return render(request, 'error.html', {'message': _("Error: no instance available. Please try again tomorrow!")})


def cancel(request, product_id):
    logic = LogicCustomers()
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = SaasProduct.objects.filter(slug = product_id).first()
    plan = LogicContracts().get_current_plan(request, product)

    # cancel the contract
    if product and logic.has_instance(customer, product):
        contract = logic.get_contract(customer, product)
        contract.auto_renew = False
        contract.save()

    return show_payment(request, product, plan, None)


def instance_view(request):
    logic = LogicCustomers()
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = LogicProducts().get_product(request)
    contract = logic.get_contract(customer, product)
    if not contract:
        return render(request, 'error.html', {'message': _("Error: no instance has been assigned yet.")})
    return render(request, 'instance.html', {'instance': contract.instance})


def display_pricing(request):
    product = LogicProducts().get_product(request)

    if product is None:
        products = LogicProducts().get_products()
        hostname = request.META['HTTP_HOST']
        if hostname.startswith("www."):
            hostname = hostname.replace('www.','')
        return render(request, 'select_product.html', {'products': products, 'hostname': hostname})

    plans = LogicPlans().get_plans(product)

    return render(request, 'pricing.html', {'product': product, 'plans': plans, 'popular_plan': plans[1].name})
