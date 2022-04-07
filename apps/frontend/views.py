from datetime import datetime
from shutil import ExecError
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
        
        return render(request, 'account.html', {'customer': customer, 'form': form, 'lang': lang, 'successmessage': _("Changes Saved")})

    return render(request, 'account.html', {'customer': customer, 'form': form, 'lang': lang})


@login_required
def plan_select(request, plan_id):
    product = LogicProducts().get_product(request)
    current_plan = LogicContracts().get_current_plan(request, product)
    plans = LogicPlans().get_plans(product)

    # the customer has selected a plan
    if plan_id != 'current':
        # check if this is a valid plan
        new_plan = LogicPlans().get_plan(product, plan_id)
        if new_plan.cost_per_period > 0:
            return show_paymentmethod(request, product, current_plan, new_plan)
        else:
            return show_contract(request, product, current_plan, new_plan)

    # load booked plan from the database
    if current_plan:
        plan_id = current_plan.slug
    else:
        plan_id = ''

    return render(request, 'plan.html', {'product': product, 'plans': plans, 'selected_plan': plan_id})

@login_required
def paymentmethod_select(request):
    product = LogicProducts().get_product(request)
    customer = SaasCustomer.objects.filter(user=request.user).first()

    if request.method == "POST":
        values = request.POST.copy()
        contract = LogicContracts().get_contract(customer, product)
        new_plan = LogicPlans().get_plan(product, values["plan"])
        if not contract:
            contract = LogicContracts().get_new_contract(customer, product, new_plan)

        contract.payment_method = values["payment_method"]
        contract.account_owner = values['account_owner']
        contract.account_iban = values['account_iban']
        if contract.payment_method == "SEPA_DIRECTDEBIT":
            if not contract.account_owner or not contract.account_iban:
                error = _("Please specify account owner and IBAN")
                return show_paymentmethod(request, product, None, None, error)

            contract.sepa_mandate_date = datetime.today()
            # TODO: something with prefixinstance_idyyyymmdd?
            contract.sepa_mandate = 'TODO'
        else:
            contract.sepa_mandate_date = None
            contract.sepa_mandate = ''
        contract.save()

        if not contract.is_confirmed or contract.plan.slug != new_plan.slug:
            return show_contract(request, product, contract.plan, new_plan)

        # confirm to user that storing worked
        return show_paymentmethod(request, product, contract.plan, None, successmessage = _("Changes Saved"))

    current_plan = LogicContracts().get_current_plan(request, product)
    if current_plan is None:
        return redirect('/plan/current')
    return show_paymentmethod(request, product, current_plan, None)


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


def show_paymentmethod(request, product, current_plan, new_plan, errormessage="", successmessage=""):
    if new_plan is None:
        new_plan = current_plan
    new_contract = new_plan != current_plan

    customer = SaasCustomer.objects.filter(user=request.user).first()
    contract = LogicContracts().get_contract(customer, product)
    if not contract:
        # get new contract from logic
        contract = LogicContracts().get_new_contract(customer, product, new_plan)

    return render(request, 'payment.html',
        {'contract': contract,
        'is_new_contract': new_contract,
        'plan': new_plan,
        'contract': contract,
        'no_payment': new_plan.cost_per_period == 0,
        'successmessage': successmessage,
        'errormessage': errormessage})


def show_contract(request, product, current_plan, new_plan):
    if new_plan is None:
        new_plan = current_plan
    customer = SaasCustomer.objects.filter(user=request.user).first()
    contract = LogicContracts().get_contract(customer, product)
    periodLength = readablePeriodsInMonths(new_plan.period_length_in_months)
    payment_invoice = contract and contract.payment_method != "SEPA_DIRECTDEBIT"
    periodLengthExtension = ''
    isFreeTest = new_plan.period_length_in_months == 0
    if new_plan.period_length_in_months == 1:
        periodLengthExtension = _("another month")
    elif new_plan.period_length_in_months == 3:
        periodLengthExtension = _("another quarter")
    elif new_plan.period_length_in_months == 12:
        periodLengthExtension = _("another year")
    isNewOrder = current_plan is None or current_plan.slug != new_plan.slug or contract.is_confirmed == False
    canCancelContract = not isNewOrder and contract.is_confirmed and contract.is_auto_renew
    noticePeriod = readablePeriodsInDays(new_plan.notice_period_in_days)
    if not contract:
        # get new contract from logic
        contract = LogicContracts().get_new_contract(customer, product, new_plan)
    else:
        # calculate new dates for this new plan; does not save the modified contract
        contract = LogicContracts().modify_contract(customer, product, new_plan)

    return render(request, 'contract.html',
        {'product': product,
        'plan': new_plan,
        'contract': contract,
        'is_new_order': isNewOrder,
        'is_free_test': isFreeTest,
        'can_cancel_contract': canCancelContract,
        'payment_invoice': payment_invoice,
        'noticePeriod': noticePeriod,
        'periodLength': periodLength,
        'periodLengthExtension': periodLengthExtension})

def contract_view(request):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = LogicProducts().get_product(request)
    contract = LogicContracts().get_contract(customer, product)
    if not contract:
        return redirect("/plan/current")

    return show_contract(request, product, contract.plan, None)

def contract_subscribe(request, product_id, plan_id):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = SaasProduct.objects.filter(slug = product_id).first()
    if not product:
        raise Exception('invalid product')
    plan = LogicPlans().get_plan(product, plan_id)
    if not plan:
        raise Exception('invalid plan')

    contract = LogicContracts().get_contract(customer, product)
    if contract and contract.is_confirmed:

        # update existing contract
        contract = LogicContracts().modify_contract(customer, product, plan)
        contract.save()

        # redirect to instance details page
        return redirect('/instance')

    else:
        # assign a new instance
        if LogicCustomers().assign_instance(customer, product, plan):
            # redirect to instance details page
            return redirect('/instance')
        else:
            # TODO what about the situation where there is no free instance available
            return render(request, 'error.html', {'message': _("Error: no instance available. Please try again tomorrow!")})


def contract_cancel(request, product_id):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = SaasProduct.objects.filter(slug = product_id).first()
    plan = LogicContracts().get_current_plan(request, product)

    if product:
        # cancel the contract
        contract = LogicContracts().get_contract(customer, product)
        if contract:
            contract.is_auto_renew = False
            contract.save()

    # show cancelled contract
    return show_contract(request, product, plan, None)


def instance_view(request):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = LogicProducts().get_product(request)
    contract = LogicContracts().get_contract(customer, product)
    if not contract or not contract.instance:
        return render(request, 'error.html', {'message': _("Error: no instance has been assigned yet.")})
    url = product.instance_url. \
            replace('#Prefix', product.prefix). \
            replace('#Identifier', contract.instance.identifier)

    return render(request, 'instance.html', {'instance': contract.instance, 'instance_url': url})


def display_pricing(request):
    product = LogicProducts().get_product(request)

    if product is None:
        products = LogicProducts().get_products()
        hostname = request.META['HTTP_HOST']
        if hostname.startswith("www."):
            hostname = hostname.replace('www.','')
        return render(request, 'select_product.html', {'products': products, 'hostname': hostname})

    plans = LogicPlans().get_plans(product)

    return render(request, 'pricing.html', {'product': product, 'plans': plans})
