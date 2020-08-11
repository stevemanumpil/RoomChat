from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib import messages
import json

from landing.models import Account
from landing.forms import *
import uuid

def index(request):
    return render(request,'index.html')

def setup_meet(request):
    id = uuid.uuid4()
    room = '/room/'+str(id.int)
    return redirect(room)

class MeetView(View):
    
    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            context['title'] = 'room'+kwargs['room_id']
            context['room_id'] = kwargs['room_id']
            return render(request, 'room_meet.html', context)

        context['title'] = 'Login'
        context['login_form'] = LoginForm()
        return render(request, 'landing/login.html', context)

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')

            user = authenticate(email=email, password=password)
            if user is not None and user.is_admin is not True:
                login(request, user)
                return redirect(request.path)

            messages.error(request, 'Invalid email or password')
            return redirect(request.path)