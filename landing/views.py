from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views import View
from landing.models import Account
from .forms import LoginForm, AccountCreationForm
from django.forms import ValidationError
from django.contrib import messages

# Create your views here.
class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')

        login_form = LoginForm()
        context = {
            'title' : 'Login',
            'login_form' : login_form
        }
        return render(request,'landing/login.html',context)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')

            user = authenticate(email=email, password=password)
            if user is not None and user.is_admin is not True:
                login(request, user)
                return redirect('/home')
            
            messages.error(request, 'Invalid email or password')
        else:
            raise ValidationError(login_form.errors)

        return redirect('/auth/login')

class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/home')

        register_form = AccountCreationForm()

        context = {
            'title' : 'Register',
            'register_form' : register_form
        }

        return render(request, 'landing/register.html', context)

    def post(self, request):
        register_form = AccountCreationForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account Successfully created')
            return redirect('/auth')

        context = {
            'title' : 'Register',
            'register_form' : register_form
        }
        return render(request, 'landing/register.html', context)
