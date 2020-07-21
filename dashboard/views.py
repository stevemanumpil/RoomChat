from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.template import loader
from django.db.models import Q
from django.views import View
from .models import Message, PersonalChat
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        context = {
            'title':'Dashboard',
            'users': User.objects.filter(~Q(username=request.user.username))
        }
        return render(request, 'dashboard/test.html', context)

    return redirect('/auth')

def chat_field(request, username):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404(f"{username} does not exist")

        context = {
            'title': 'Chat',
            'users': User.objects.filter(~Q(username=request.user.username)),
            'username' : user.username
        }
        return render(request, 'dashboard/test.html', context)

def req(request, user_id):
    if request.method == 'GET':
        user = User.objects.get(id=user_id)
        template = loader.get_template('dashboard/include/chat_field.html')
        return HttpResponse(template.render({'username':user.first_name+' '+user.last_name}, request))

    raise Http404("gak ada")

def store(request):
    return HttpResponse(JsonResponse(request, safe=False))

def Logout(request):
    logout(request)
    return redirect('/')

class StoreView(View):

    def get(self, request, *args, **kwargs):
        try:
            dest = User.objects.get(username=kwargs['username'])
            pc_id = PersonalChat.objects.get(Q(user1__in=[request.user,dest]) & Q(user2__in=[dest, request.user])).id
            messages = list(Message.objects.filter(pc_id=pc_id).values('user_id','text'))
            for prop in messages:
                if prop['user_id'] == request.user.id:
                    prop['position'] = 'end'
                    prop['user'] = request.user.username
                else:
                    prop['position'] = 'start'
                    prop['user'] = kwargs['username']

                prop.pop("user_id")

            data = json.dumps({'response': messages})
            return HttpResponse(data)
        except ObjectDoesNotExist:
            data = json.dumps({'response':'object does not exist'})
            return HttpResponse(data)

    def post(self, request):

        resp = json.loads(request.body)
        dest = User.objects.get(username=resp['dest'])
        pc_id = list(PersonalChat.objects.filter(Q(user1__in=[request.user,dest]) & Q(user2__in=[dest,request.user])))

        if pc_id:
            self.store(pc_id[0], resp, request.user)
        else:
            pc = PersonalChat()
            pc.user1 = request.user
            pc.user2 = dest
            pc.save()
            self.store(pc, resp, request.user)

        return HttpResponse(JsonResponse(resp, safe=False))

    def store(self, pc, resp, user):
        message = Message()
        message.user_id = user
        message.text = resp["msg"]
        message.date_send = datetime.now()
        message.pc_id = pc
        message.save()


class PanelView(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=kwargs['username'])
        template = loader.get_template('dashboard/include/chat_field.html')
        return HttpResponse(template.render({'username':user.first_name}, request))
