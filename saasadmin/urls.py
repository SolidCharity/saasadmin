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
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', backend_views.home),
    path('home/', backend_views.home),
    path('', include('apps.api.urls')),
    path('plans/add', backend_views.addplan),
    path('plans/edit/<int:id>', backend_views.editplan),
    path('plans/update/<int:id>', backend_views.updateplan),
    path('plans/delete/<int:id>', backend_views.deleteplan),

    path('frontend/login', frontend_views.login_view),
    path('frontend/account', frontend_views.account_view),
    path('frontend/logout', frontend_views.logout_view),
    path('frontend/register', frontend_views.register_view),
    path('frontend/plans', frontend_views.display_plans),

    # paths for testing the frontend locally
    path('en/sign-in/', frontend_views.login_view),
    path('en/register/', frontend_views.register_view),
    path('en/account/', frontend_views.account_view),
    path('en/logout/', frontend_views.logout_view),

]
