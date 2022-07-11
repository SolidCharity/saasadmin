"""saasadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from apps.admin import views as admin_views
from apps.customer import views as customer_views

urlpatterns = [
    # Django urls
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),

    # API
    path('', include('apps.api.urls')),

    # i18n
    path('i18n/', include('django.conf.urls.i18n')),

    # SaasAdmin Admin UI
    path('customers/<str:product>/', admin_views.customers),
    path('instances/<str:product>/', admin_views.instances),
    path('instances/<str:product>/add', admin_views.addinstances),
    path('plans/<str:product>/', admin_views.plans),
    path('plans/<str:product>/preview', admin_views.preview_pricing),
    path('plans/<str:product>/add', admin_views.addplan),
    path('plans/edit/<int:id>', admin_views.editplan),
    path('plans/update/<int:id>', admin_views.updateplan),
    path('plans/delete/<int:id>', admin_views.deleteplan),
    path('contracts/edit/<int:id>/<str:newplan>', admin_views.editcontract),

    path('products/list', admin_views.products),
    path('products/add', admin_views.addproduct),
    path('products/<str:slug>/dashboard', admin_views.productdashboard),
    path('products/edit/<int:id>', admin_views.editproduct),
    path('products/update/<int:id>', admin_views.updateproduct),
    path('products/delete/<int:id>', admin_views.deleteproduct),

    path('configurations/', admin_views.configurations),
    path('configurations/add', admin_views.addconfiguration),
    path('configurations/edit/<int:id>', admin_views.editconfiguration),
    path('configurations/update/<int:id>', admin_views.updateconfiguration),

    path('instances/edit/<int:id>', admin_views.editinstance),
    path('instances/update/<int:id>', admin_views.updateinstance),

    # SaasAdmin Customer UI
    path('', customer_views.home),
    path('home/', customer_views.home),
    path('account', customer_views.account_view),
    path('account/update', customer_views.account_update),
    path('plan/current', customer_views.display_plans),
    path('plan/select/<str:plan_id>', customer_views.plan_select),
    path('paymentmethod', customer_views.paymentmethod_select),
    path('contract', customer_views.contract_view),
    path('contract/add/<str:product_id>/<str:plan_id>', customer_views.contract_subscribe),
    path('contract/cancel/<str:product_id>', customer_views.contract_cancel),
    path('products', customer_views.display_products),
    path('instance', customer_views.instance_view),
    path('pricing', customer_views.display_pricing),
    path('imprint', customer_views.display_imprint),
    path('about', customer_views.display_about),
    path('contact', customer_views.display_contact),

]