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

    # SaasAdmin Backend
    path('backend', backend_views.plans),
    path('customers', backend_views.customers),
    path('instances', backend_views.instances),
    path('plans', backend_views.plans),
    path('plans/add', backend_views.addplan),
    path('plans/edit/<int:id>', backend_views.editplan),
    path('plans/update/<int:id>', backend_views.updateplan),
    path('plans/delete/<int:id>', backend_views.deleteplan),

    # SaasAdmin Frontend
    path('', frontend_views.home),
    path('home/', frontend_views.home),
    path('account', frontend_views.account_view),
    path('account/update', frontend_views.account_update),
    path('plan/<str:plan_id>', frontend_views.select_plan),
    path('payment', frontend_views.select_payment),
    path('pricing', frontend_views.display_pricing),
]
