from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse

def home(request):
    # if not logged in => redirect to login screen
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if request.user.is_staff:
        return redirect('/backend')
    # if logged in customer => redirect frontend view
    return redirect('/account')

@login_required
def account_view(request):
    lang="en"
    # TODO pass user details
    return render(request, 'account.html', {'lang': lang})

@login_required
def select_plan(request):
    return render(request, 'product.html', {})

@login_required
def select_payment(request):
    return render(request, 'payment.html', {})

def display_pricing(request):
    return render(request, 'pricing.html', {})
