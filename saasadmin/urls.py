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
from apps.backend import views as backend_views
from apps.frontend import views as frontend_views

urlpatterns = [
    # Django urls
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django_registration.backends.activation.urls')),

    # API
    path('', include('apps.api.urls')),

    # i18n
    path('i18n/', include('django.conf.urls.i18n')),

    # SaasAdmin Backend
    path('backend', backend_views.products),
    path('customers/<str:product>/', backend_views.customers),
    path('instances/<str:product>/', backend_views.instances),
    path('instances/<str:product>/add', backend_views.addinstances),
    path('plans/<str:product>/', backend_views.plans),
    path('plans/<str:product>/preview', backend_views.preview_pricing),
    path('plans/<str:product>/add', backend_views.addplan),
    path('plans/edit/<int:id>', backend_views.editplan),
    path('plans/update/<int:id>', backend_views.updateplan),
    path('plans/delete/<int:id>', backend_views.deleteplan),
    path('contracts/edit/<int:id>/<str:newplan>', backend_views.editcontract),

    path('products', backend_views.products),
    path('products/add', backend_views.addproduct),
    path('products/<str:slug>/dashboard', backend_views.productdashboard),
    path('products/edit/<int:id>', backend_views.editproduct),
    path('products/update/<int:id>', backend_views.updateproduct),
    path('products/delete/<int:id>', backend_views.deleteproduct),

    path('configurations/', backend_views.configurations),
    path('configurations/add', backend_views.addconfiguration),
    path('configurations/edit/<int:id>', backend_views.editconfiguration),
    path('configurations/update/<int:id>', backend_views.updateconfiguration),

    path('instances/edit/<int:id>', backend_views.editinstance),
    path('instances/update/<int:id>', backend_views.updateinstance),

    # SaasAdmin Frontend
    path('', frontend_views.home),
    path('home/', frontend_views.home),
    path('account', frontend_views.account_view),
    path('account/update', frontend_views.account_update),
    path('plan/<str:plan_id>', frontend_views.plan_select),
    path('paymentmethod', frontend_views.paymentmethod_select),
    path('contract', frontend_views.contract_view),
    path('contract/add/<str:product_id>/<str:plan_id>', frontend_views.contract_subscribe),
    path('contract/cancel/<str:product_id>', frontend_views.contract_cancel),
    path('instance', frontend_views.instance_view),
    path('pricing', frontend_views.display_pricing),
    path('imprint', frontend_views.display_imprint),
    path('about', frontend_views.display_about),
    path('contact', frontend_views.display_contact),

]