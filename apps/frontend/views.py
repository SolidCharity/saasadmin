from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse

def login_view(request):
    lang = "en"
    if request.method == "POST":
        values = request.POST.copy()
        lang = values['lang']
        user = authenticate(request=request, username=values['email'], password=values['password'])
        if user is None:
            result = { 'status': 'failure', 'errormsg': 'TODO ERROR' }
            return JsonResponse(result)
        login(request, user)
        result = { 'status': 'success', 'statusmsg': 'TODO SUCCESS' }
        response = render(request, 'json.html', result)
        response["Content-Type"] = "application/json"
        return response
        response = JsonResponse(result)
        response.set_cookie(request.COOKIES.get('session_id'))
        return response

    return render(request, 'login.html', {'lang': lang})

def account_view(request):
    lang="en"
    # is the user logged in?
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'lang': lang})
    # TODO pass user details
    return render(request, 'account.html', {'lang': lang})

def logout_view(request):
    logout(request)
    lang="en"
    return render(request, 'login.html', {'lang': lang})

def register_view(request):
    lang = "en"
    if request.method == "POST":
        values = request.POST.copy()
        lang = values['lang']
        try:
            # TODO password check, 2nd passwort. password policy; store user name
            user = User.objects.create_user(values['email'], values['email'], values['password'])
        except IntegrityError:
            user = None
        if not user:
            result = { 'status': 'failure', 'errormsg': 'TODO ERROR' }
            return JsonResponse(result)
            return render(request, 'register.html', {'errormsg': 'TODO ERROR'})
        result = { 'status': 'success', 'statusmsg': 'TODO SUCCESS' }
        return JsonResponse(result)

    return render(request, 'register.html', {'lang': lang})

def display_plans(request):
    return render(request, 'product.html', {})
