from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from apps.core.models import SaasInstance
from apps.core.models import SaasCustomer
from apps.core.models import SaasPlan
from apps.core.models import SaasProduct
from apps.backend.forms import PlanForm, ProductForm, AddInstancesForm
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

        sql = """SELECT email_address, first_name, last_name, saas_instance.identifier as instance_identifier
            FROM saas_customer, saas_instance, saas_contract
            WHERE saas_contract.customer_id = saas_customer.id
            AND saas_contract.instance_id = saas_instance.id
            AND saas_instance.product_id = %s"""

        cursor.execute(sql, [product.id,])
        result = cursor.fetchall()

        customers = []
        for row in result:
            # create an associative array
            a = dict(zip([c[0] for c in cursor.description], row))
            # create an object
            o = namedtuple("customer", a.keys())(*a.values())
            # add the object to resulting array
            customers.append(o)

    return render(request,"customers.html",
            {'customers': customers, 'product': product})

@login_required
@staff_member_required
def instances(request, product):
    product = SaasProduct.objects.filter(slug = product).first()
    unused_instances = SaasInstance.objects.filter(product = product).filter(Q(status='free') | Q(status='in_preparation'))

    return render(request,"instances.html",
            {'unused_instances': unused_instances, 'product': product })


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
                for x in range(1, int(form['count'].value())):
                    success, new_data = LogicInstances().create_new_instance(form['hostname'].value(), product)
                    if not success:
                        raise Exception('there was an error creating a new instance')
                return redirect("/instances/%s/" % (product.slug,))
            except Exception as ex:
                print('Exception in addinstances: %s' % (ex,))
                pass
    else:
        # use the last used hostname for this product
        hostname = 'localhost'
        last_instance = SaasInstance.objects.filter(product=product).order_by('id')
        if last_instance.count() > 0:
            hostname = last_instance.last().hostname
        form = AddInstancesForm(initial={'product_id': product.id, 'count': 10, 'hostname': hostname})

    return render(request,'addinstances.html',{'form': form, 'product': product})


@login_required
@staff_member_required
def plans(request, product):
    product = SaasProduct.objects.filter(slug = product).first()
    plans = SaasPlan.objects.filter(product = product)

    return render(request,"plans.html",
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
        return redirect("/products")
    return render(request, 'editproduct.html', {'product': product, 'form': form})

@login_required
@staff_member_required
def deleteproduct(request, id):
    product = SaasProduct.objects.get(id=id)
    product.delete()
    return redirect("/products")
