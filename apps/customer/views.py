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
from apps.core.models import SaasCustomer, SaasPlan, SaasProduct, SaasConfiguration
from apps.customer.forms import CustomerForm
from apps.api.logic.customers import LogicCustomers
from apps.api.logic.plans import LogicPlans
from apps.api.logic.contracts import LogicContracts

def home(request):
    if request.user.is_staff:
        return redirect('/products/list')
    product = LogicProducts().get_product(request, False)
    if product is None:
        return redirect('/products')
    # if not logged in => redirect to pricing
    if not request.user.is_authenticated:
        return display_pricing(request)

    # if logged in customer => redirect customer view
    customer = SaasCustomer.objects.filter(user=request.user).first()
    if not customer:
        # first login: need to create customer first
        return redirect('/account')

    return redirect('/plan/current')

@login_required
def account_view(request):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    if customer is None:
        # create a new customer for this user
        customer = SaasCustomer()
        customer.user = request.user
        customer.email_address = request.user.email
        customer.save()

    form = CustomerForm(instance = customer)
    return render(request, 'account.html', {'customer': customer, 'form': form})

def  clean_null(customer):
    if customer.organisation_name is None:
        customer.organisation_name = ''
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

    customer = SaasCustomer.objects.filter(user=request.user).first()
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    values['user'] = request.user.id

    form = CustomerForm(values, instance = customer)
    if form.is_valid():
        form.save()
        
        return render(request, 'account.html', {'customer': customer, 'form': form, 'successmessage': _("Changes Saved")})

    return render(request, 'account.html', {'customer': customer, 'form': form})


@login_required
def display_plans(request):
    product = LogicProducts().get_product(request, False)
    if product is None:
        return redirect('/products')
    current_contract = LogicContracts().get_current_contract(request, product)
    if current_contract:
        current_plan = current_contract.plan
    else:
        current_plan = None
    if current_plan is None and not product.is_active:
        product = None
    plans = LogicPlans().get_plans(product)

    storage={}
    for plan in plans:
        if plan.cost_for_storage:
            storage[plan.id] = {}
            IncludedStorageSizeInGB = plan.get_included_storage_gb()
            storage[plan.id][0] = _("{} GB is included in price").format(IncludedStorageSizeInGB)
            for x in range(1, 10):
                AdditionalSizeInGB = plan.get_additional_storage_gb()*x
                additional_cost= plan.cost_for_storage*x

                if plan.currency_code == "EUR":
                    currency_symbol = '€'
                else:
                    currency_symbol = plan.currency_code

                storage[plan.id][AdditionalSizeInGB]=_("+ {} GB costs +{} {}").format(AdditionalSizeInGB, additional_cost, currency_symbol)
            storage[plan.id][999] = _("Contact us if you need more")

    if current_contract and current_contract.instance:
        selected_additional_storage = current_contract.instance.additional_storage
    else:
        selected_additional_storage = None

    # load booked plan from the database
    if current_plan:
        plan_id = current_plan.slug
    else:
        plan_id = ''

    return render(request, 'plan.html', {'product': product, 'plans': plans, 'storage':storage ,'selected_plan': plan_id, 'selected_additional_storage': selected_additional_storage})


@login_required
def plan_select(request, plan_id):
    product = LogicProducts().get_product(request, False)
    if product is None:
        return redirect('/products')
    current_plan = LogicContracts().get_current_plan(request, product)
    if current_plan is None and not product.is_active:
        product = None
    plans = LogicPlans().get_plans(product)

    if "additional_storage" in request.POST:
        additional_storage = request.POST["additional_storage"]
    else:
        additional_storage = 0
    if additional_storage == "999":
        return display_plans(request)

    # check if this is a valid plan
    new_plan = LogicPlans().get_plan(product, plan_id)

    if new_plan.cost_per_period > 0:
        return show_paymentmethod(request, product, current_plan, new_plan, additional_storage=additional_storage)
    else:
        return show_contract(request, product, current_plan, new_plan, additional_storage)


@login_required
def paymentmethod_select(request):
    product = LogicProducts().get_product(request, False)
    customer = SaasCustomer.objects.filter(user=request.user).first()
    contract = LogicContracts().get_contract(customer, product)

    if request.method == "POST":
        if "additional_storage" in request.POST:
            additional_storage = int(request.POST["additional_storage"])
        else:
            additional_storage = 0

        values = request.POST.copy()
        new_plan = LogicPlans().get_plan(product, values["plan"])
        if not contract:
            contract = LogicContracts().get_new_contract(customer, product, new_plan, 0)

        contract.payment_method = values["payment_method"]
        contract.account_owner = values['account_owner']
        contract.account_iban = values['account_iban']
        if contract.payment_method == "SEPA_DIRECTDEBIT":
            if not contract.account_owner or not contract.account_iban:
                error = _("Please specify account owner and IBAN")
                return show_paymentmethod(request, product, None, None, additional_storage=additional_storage, errormessage=error)

            contract.sepa_mandate_date = datetime.today()
            contract.sepa_mandate = f"{contract.instance.identifier}{contract.sepa_mandate_date:%Y%m%d}"
        else:
            contract.sepa_mandate_date = None
            contract.sepa_mandate = ''
        contract.save()

        if not contract.is_confirmed or contract.plan.slug != new_plan.slug or contract.instance.additional_storage != additional_storage:
            return show_contract(request, product, contract.plan, new_plan, additional_storage)

        # confirm to user that storing worked
        return show_paymentmethod(request, product, contract.plan, None, additional_storage=additional_storage, successmessage = _("Changes Saved"))

    current_plan = LogicContracts().get_current_plan(request, product)
    if current_plan is None:
        return redirect('/plan/current')
    return show_paymentmethod(request, product, current_plan, None, additional_storage=contract.instance.additional_storage)


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
    elif periodLength == 1:
        return "1 " + _("day")
    else:
        return str(periodLength) + " " + _("days")


def show_paymentmethod(request, product, current_plan, new_plan, additional_storage=0, errormessage="", successmessage=""):
    if new_plan is None:
        new_plan = current_plan
    new_contract = new_plan != current_plan

    customer = SaasCustomer.objects.filter(user=request.user).first()
    contract = LogicContracts().get_contract(customer, product)
    if not contract:
        # get new contract from logic
        contract = LogicContracts().get_new_contract(customer, product, new_plan, 0)

    return render(request, 'payment.html',
        {'contract': contract,
        'is_new_contract': new_contract,
        'plan': new_plan,
        'contract': contract,
        'additional_storage': additional_storage,
        'no_payment': new_plan.cost_per_period == 0,
        'successmessage': successmessage,
        'errormessage': errormessage})


def show_contract(request, product, current_plan, new_plan, additional_storage):
    if new_plan is None:
        new_plan = current_plan
    customer = SaasCustomer.objects.filter(user=request.user).first()
    contract = LogicContracts().get_contract(customer, product)
    if new_plan.period_length_in_months > 0:
        periodLength = readablePeriodsInMonths(new_plan.period_length_in_months)
    elif new_plan.period_length_in_days > 0:
        periodLength = readablePeriodsInDays(new_plan.period_length_in_days)
    else:
        periodLength = _("forever")
    payment_invoice = contract and contract.payment_method != "SEPA_DIRECTDEBIT"
    periodLengthExtension = ''
    isFreeTest = new_plan.cost_per_period == 0
    isUnlimitedTest = isFreeTest and new_plan.period_length_in_months == 0 and new_plan.period_length_in_days == 0
    if new_plan.period_length_in_months == 1:
        periodLengthExtension = _("another month")
    elif new_plan.period_length_in_months == 3:
        periodLengthExtension = _("another quarter")
    elif new_plan.period_length_in_months == 12:
        periodLengthExtension = _("another year")
    isNewOrder = (current_plan is None
        or current_plan.slug != new_plan.slug
        or contract.instance is None
        or contract.instance.additional_storage != additional_storage
        or contract.is_confirmed == False)
    canCancelContract = not isNewOrder and contract.is_confirmed and contract.is_auto_renew
    noticePeriod = readablePeriodsInDays(new_plan.notice_period_in_days)
    if not contract:
        # get new contract from logic
        contract = LogicContracts().get_new_contract(customer, product, new_plan, 0)
    else:
        # calculate new dates for this new plan; does not save the modified contract
        contract = LogicContracts().modify_contract(customer, product, new_plan)

    if additional_storage:
        additional_storage_cost = int(additional_storage)/new_plan.get_additional_storage_gb() * float(new_plan.cost_for_storage)
    else:
        additional_storage_cost = 0

    return render(request, 'contract.html',
        {'product': product,
        'plan': new_plan,
        'contract': contract,
        'is_new_order': isNewOrder,
        'is_free_test': isFreeTest,
        'is_unlimited_test': isUnlimitedTest,
        'can_cancel_contract': canCancelContract,
        'payment_invoice': payment_invoice,
        'additional_storage': additional_storage,
        'additional_storage_cost': additional_storage_cost,
        'noticePeriod': noticePeriod,
        'periodLength': periodLength,
        'periodLengthExtension': periodLengthExtension})

@login_required
def contract_view(request):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = LogicProducts().get_product(request, False)
    contract = LogicContracts().get_contract(customer, product)
    if not contract:
        return redirect("/plan/current")

    return show_contract(request, product, contract.plan, None, contract.instance.additional_storage)

@login_required
def contract_subscribe(request, product_id, plan_id):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = SaasProduct.objects.filter(slug = product_id).first()
    if not product:
        raise Exception('invalid product')
    plan = LogicPlans().get_plan(product, plan_id)
    if not plan:
        raise Exception('invalid plan')

    if "additional_storage" in request.POST:
        additional_storage = request.POST["additional_storage"]
    else:
        additional_storage = 0

    contract = LogicContracts().get_contract(customer, product)
    if contract and contract.is_confirmed:

        # update existing contract
        contract = LogicContracts().modify_contract(customer, product, plan)
        contract.save()

        # send email to admin
        LogicCustomers().notify_administrators(_("Contract for %s upgraded") % (product.name,),
                _("Nice, a contract of %s was upgraded for customer %d") % (product.name, customer.id))

        if additional_storage:
            instance = contract.instance
            if instance.additional_storage != additional_storage:
                instance.additional_storage = additional_storage
                instance.save()

        # redirect to instance details page
        return redirect('/instance')

    else:
        # assign a new instance
        if LogicCustomers().assign_instance(customer, product, plan, additional_storage):
            # redirect to instance details page
            return redirect('/instance')
        else:
            # TODO what about the situation where there is no free instance available
            return render(request, 'error.html', {'message': _("Error: no instance available. Please try again tomorrow!")})

@login_required
def contract_cancel(request, product_id):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = SaasProduct.objects.filter(slug = product_id).first()
    contract = LogicContracts().get_contract(customer, product)
    plan = contract.plan

    # cancel the contract
    if contract and contract.is_auto_renew:
        contract.is_auto_renew = False
        contract.save()

    # show cancelled contract
    return show_contract(request, product, plan, None, None)

@login_required
def instance_view(request):
    customer = SaasCustomer.objects.filter(user=request.user).first()
    product = LogicProducts().get_product(request, False)
    if product is None:
        return redirect('/products')
    contract = LogicContracts().get_contract(customer, product)
    if not contract or not contract.instance:
        return render(request, 'error.html', {'message': _("Error: no instance has been assigned yet.")})
    if contract.instance.custom_domain:
        url = f"https://{contract.instance.custom_domain}/"
    else:
        url = product.instance_url. \
            replace('#Prefix', product.prefix). \
            replace('#Identifier', contract.instance.identifier)
    pwd_reset_url = product.instance_password_reset_url. \
            replace('#EmailAddress', customer.email_address)
    initialadminpassword = ''
    if pwd_reset_url == 'password1':
        # Tryton does not have a password reset functionality for the admin user
        initialadminpassword = contract.instance.password1
        pwd_reset_url = None
    elif pwd_reset_url.startswith('/'):
        pwd_reset_url = url + pwd_reset_url[1:]
    login_url = url
    if product.login_url.startswith('/'):
        login_url = url + product.login_url[1:]
    adminuser = product.instance_admin_user
    adminemail = customer.email_address

    return render(request, 'instance.html',
        {'instance': contract.instance,
        'instance_url': url,
        'login_url': login_url,
        'adminuser': adminuser,
        'adminemail': adminemail,
        'initialadminpassword': initialadminpassword,
        'pwd_reset_url': pwd_reset_url})


def display_products(request):
    products = LogicProducts().get_products()
    count = 1
    for product in products:
        if count % 4 == 0:
            product.newrow = True
        count += 1

    return render(request, 'select_product.html', {'products': products})


def display_pricing(request):
    product = LogicProducts().get_product(request)

    if product is None:
        return display_products(request)

    plans = LogicPlans().get_plans(product)

    return render(request, 'pricing.html', {'product': product, 'plans': plans})

def display_imprint(request):
    conf = SaasConfiguration.objects.filter(name='imprint').first()
    return render(request, 'display_value.html', {'conf': conf})

def display_about(request):
    conf = SaasConfiguration.objects.filter(name='about').first()
    return render(request, 'display_value.html', {'conf': conf})

def display_contact(request):
    conf = SaasConfiguration.objects.filter(name='contact').first()
    if not conf:
        return None
    conf.value = conf.value.replace('#Website', request.get_host())
    return render(request, 'display_value.html', {'conf': conf})



