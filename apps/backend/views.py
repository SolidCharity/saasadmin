from datetime import timedelta, date
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.translation import gettext as _
from apps.core.models import SaasContract, SaasCustomer, SaasInstance, SaasPlan, SaasProduct, SaasConfiguration, SaasInstance
from apps.core.models import SaasConfiguration
from apps.backend.forms import PlanForm, ProductForm, AddInstancesForm, ConfigurationForm, InstanceForm
from apps.api.logic.contracts import LogicContracts
from apps.api.logic.products import LogicProducts
from apps.api.logic.instances import LogicInstances
from django.db.models import Q
from django.db import connection
from collections import namedtuple


@login_required
@staff_member_required
def customers(request, product):
    product = SaasProduct.objects.filter(slug = product).first()
    with connection.cursor() as cursor:

        sql = """SELECT email_address, first_name, last_name,
            saas_instance.identifier as instance_identifier,
            sc.id as contract_id,
            saas_instance.id as instance_id,
            sc.end_date as contract_end_date,
            sc.is_auto_renew as contract_auto_renew,
            saas_plan.name as plan_name,
            sc.plan_id
            FROM saas_customer, saas_instance, saas_contract sc, saas_plan
            WHERE sc.customer_id = saas_customer.id
            AND sc.instance_id = saas_instance.id
            AND sc.plan_id = saas_plan.id
            AND (sc.end_date is NULL or sc.end_date > current_timestamp)
            AND saas_instance.product_id = %s"""

        cursor.execute(sql, [product.id,])
        result = cursor.fetchall()

        customers = []
        for row in result:
            # create an associative array
            a = dict(zip([c[0] for c in cursor.description], row))
            if a['contract_auto_renew']:
                a['contract_finish'] = _('contract will be auto renewed')
            elif not a['contract_end_date']:
                a['contract_finish'] = _('contract is indefinite')
            else:
                a['contract_finish'] = _('contract ends on %s') % a['contract_end_date']
            plan = SaasPlan.objects.get(id=a['plan_id'])
            a['plan_name'] = plan.name
            a['plan_cost'] = plan.cost_per_period
            # create an object
            o = namedtuple("customer", a.keys())(*a.values())
            # add the object to resulting array
            customers.append(o)

    return render(request,"customers.html",
            {'customers': customers, 'product': product})


@login_required
@staff_member_required
def editcontract(request, id, newplan):
    contract = SaasContract.objects.get(id=id)
    plan = contract.plan

    if plan.cost_per_period == 0:
        if newplan == "AddTest14":
            contract.end_date += timedelta(days=14)
            contract.save()
        elif newplan == "MakeFree" and not contract.end_date is None:
            # find the plan that has no limit and is free
            freeplan = SaasPlan.objects.filter(product = plan.product, cost_per_period = 0, period_length_in_months=0, period_length_in_days=0).first()
            if freeplan:
                contract.end_date = None
                contract.plan_id = freeplan.id
                contract.save()

    return redirect("/customers/%s/" % (plan.product.slug,))


@login_required
@staff_member_required
def instances(request, product):
    product = SaasProduct.objects.filter(slug = product).first()
    unused_instances = SaasInstance.objects.filter(product = product).filter(Q(status=SaasInstance().AVAILABLE) | Q(status=SaasInstance().READY) | Q(status=SaasInstance().IN_PREPARATION))
    to_be_removed_instances = SaasInstance.objects.filter(product = product).filter(status=SaasInstance().TO_BE_REMOVED)

    return render(request,"instances.html",
            {'unused_instances': unused_instances,
             'to_be_removed_instances': to_be_removed_instances,
             'product': product })


@login_required
@staff_member_required
def addinstances(request, product):
    product = SaasProduct.objects.filter(slug = product).first()

    if request.method == "POST":
        # request.POST is immutable, so make a copy
        values = request.POST.copy()
        form = AddInstancesForm(values)
        if form.is_valid():
            try:
                for x in range(0, int(form['count'].value())):
                    success, new_data = LogicInstances().create_new_instance(form['hostname'].value(), form['pacuser'].value(), product)
                    if not success:
                        raise Exception('there was an error creating a new instance')
                return redirect("/instances/%s/" % (product.slug,))
            except Exception as ex:
                print('Exception in addinstances: %s' % (ex,))
                raise
    else:
        # use the last used hostname for this product
        hostname = 'localhost'
        pacuser = 'xyz00'
        last_instance = SaasInstance.objects.filter(product=product).order_by('id')
        if last_instance.count() > 0:
            hostname = last_instance.last().hostname
            pacuser = last_instance.last().pacuser
        form = AddInstancesForm(initial={'product_id': product.id, 'count': 10, 'hostname': hostname, 'pacuser': pacuser})

    return render(request,'addinstances.html',{'form': form, 'product': product})


@login_required
@staff_member_required
def plans(request, product):
    product = SaasProduct.objects.filter(slug = product).first()
    plans = SaasPlan.objects.filter(product = product).order_by('cost_per_period').order_by('priority')

    return render(request,"plans.html",
            { 'plans': plans, 'product': product })

@login_required
@staff_member_required
def preview_pricing(request, product):
    product = SaasProduct.objects.filter(slug = product).first()
    plans = SaasPlan.objects.filter(product = product).order_by('cost_per_period').order_by('priority')

    return render(request,"pricing.html",
            { 'plans': plans, 'product': product })

@login_required
@staff_member_required
def addplan(request, product):
    product = SaasProduct.objects.filter(slug = product).first()

    if request.method == "POST":
        # request.POST is immutable, so make a copy
        values = request.POST.copy()
        values['owner'] = request.user.id
        form = PlanForm(values)
        if form.is_valid():
            try:
                form.instance.product = product
                form.save()
                return redirect("/plans/%s/" % (product.slug,))
            except:
                pass
    else:
        form = PlanForm()
    return render(request,'addplan.html',{'form': form, 'product': product})

@login_required
@staff_member_required
def editplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    form = PlanForm(request.POST or None, instance = plan)
    return render(request,'editplan.html', {'plan':plan, 'form': form, 'product': plan.product})

@login_required
@staff_member_required
def updateplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    form = PlanForm(values, instance = plan)
    if form.is_valid():
        form.save()
        return redirect("/plans/%s/" % (plan.product.slug,))
    return render(request, 'editplan.html', {'plan': plan, 'form': form})

@login_required
@staff_member_required
def deleteplan(request, id):
    plan = SaasPlan.objects.get(id=id)
    plan.delete()
    return redirect("/plans/%s/" % (plan.product.slug,))

@login_required
@staff_member_required
def products(request):
    products = SaasProduct.objects.all()
    product = LogicProducts().get_product(request, False)

    return render(request,"products.html",
            { 'products': products, 'product': product })

@login_required
@staff_member_required
def addproduct(request):

    if request.method == "POST":
        # request.POST is immutable, so make a copy
        values = request.POST.copy()
        values['owner'] = request.user.id
        form = ProductForm(values)
        if form.is_valid():
            try:
                form.save()
                return redirect('/products')
            except:
                pass
    else:
        form = ProductForm()
    return render(request,'addproduct.html',{'form':form})

@login_required
@staff_member_required
def productdashboard(request, slug):
    product = SaasProduct.objects.filter(slug=slug).first()
    return render(request,'productdashboard.html', {'product':product})


@login_required
@staff_member_required
def editproduct(request, id):
    product = SaasProduct.objects.get(id=id)
    form = ProductForm(request.POST or None, instance = product)
    return render(request,'editproduct.html', {'product':product, 'form': form})

@login_required
@staff_member_required
def updateproduct(request, id):
    product = SaasProduct.objects.get(id=id)
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    form = ProductForm(values, instance = product)
    if form.is_valid():
        form.save()
        return productdashboard(request, product.slug)
    return render(request, 'editproduct.html', {'product': product, 'form': form})

@login_required
@staff_member_required
def deleteproduct(request, id):
    product = SaasProduct.objects.get(id=id)
    product.delete()
    return redirect("/products")

@login_required
@staff_member_required
def configurations(request):
    configurations = SaasConfiguration.objects.all()

    return render(request,"configurations.html",
            { 'configurations': configurations })

@login_required
@staff_member_required
def addconfiguration(request):
    if request.method == "POST":
        # request.POST is immutable, so make a copy
        values = request.POST.copy()
        form = ConfigurationForm(values)
        if form.is_valid():
            try:
                form.save()
                return redirect("/configurations/")
            except:
                pass
    else:
        form = ConfigurationForm()
    return render(request,'addconfiguration.html',{'form': form})

@login_required
@staff_member_required
def editconfiguration(request, id):
    configuration = SaasConfiguration.objects.get(id=id)
    form = ConfigurationForm(request.POST or None, instance = configuration)
    return render(request,'editconfiguration.html', {'configuration':configuration, 'form': form})

@login_required
@staff_member_required
def updateconfiguration(request, id):
    configuration = SaasConfiguration.objects.get(id=id)
    form = ConfigurationForm(request.POST or None, instance = configuration)
    if form.is_valid():
        form.save()
        return redirect("/configurations")
    return render(request, 'editconfiguration.html', {'configuration': configuration, 'form': form})

@login_required
@staff_member_required
def editinstance(request, id):
    instance = SaasInstance.objects.get(id=id)
    form = InstanceForm(request.POST or None, instance = instance)
    return render(request,'editinstance.html', {'instance':instance, 'form': form})

@login_required
@staff_member_required
def updateinstance(request, id):
    instance = SaasInstance.objects.get(id=id)
    # request.POST is immutable, so make a copy
    values = request.POST.copy()
    form = InstanceForm(values, instance = instance)
    if form.is_valid():
        form.save()
        return redirect(f"/customers/{instance.product.slug}/")
    return render(request, 'editinstance.html', {'instance': instance, 'form': form})
