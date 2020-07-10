from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    context = {
        'title': 'Login'
    }
    return render(request, 'login.html', context)


def check(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/home')

    return redirect('/auth/')


def register(request):
    context = {
        'title': 'Register'
    }
    return render(request, 'register.html', context)


def save(request):
    pas1 = request.POST.get('password')
    pas2 = request.POST.get('conf_password')

    if request.method == 'POST' and pas1 == pas2:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get("email")
        password = request.POST.get('password')

        user = User.objects.create_user(first_name, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/auth/')

    return redirect('/')
