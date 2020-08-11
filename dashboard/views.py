from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth import logout
from landing.models import Account
from django.template import loader
from django.views import View
from django.db.models import Q, F
from .models import *
from django.core.exceptions import ObjectDoesNotExist
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        context = {
            'title':'Dashboard',
            'chats': Room.objects.filter(participant__username=request.user.username),
            'contact' : Account.objects.exclude(username__in=['admin',request.user.username])
        }
        return render(request, 'dashboard/include/base.html', context)
        
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

def check(request):
    resp = json.loads(request.body)
    
    if Room.objects.filter(participant__username=request.user.username, tipe='Pr').get(participant__username=resp['dest']):
        data = json.dumps({'response':'exist'})
    
    
    return HttpResponse(data)

def Logout(request):
    logout(request)
    return redirect('/')

class StoreView(View):

    def get(self, request, *args, **kwargs):
        try:
            room = Room.objects.get(name=kwargs['name'])

            messages = list(Message.objects.filter(room=room).values('sender','text'))
            participant = list(room.participant.exclude(username=request.user.username).values('username'))

            for prop in messages:
                if prop['sender'] == request.user.id:
                    prop['position'] = 'end'
                    prop['user'] = request.user.username
                else:
                    prop['position'] = 'start'
                    prop['user'] = room.participant.get(pk=prop['sender']).username

                prop.pop('sender')

            data = json.dumps({'response': messages, 'participant':participant})
            # pc_id = PersonalChat.objects.get(Q(user1__in=[request.user,dest]) & Q(user2__in=[dest, request.user]))
            # messages = list(Message.objects.filter(pc_id=pc_id).values('user_id','text'))
            # for prop in messages:
            #     if prop['user_id'] == request.user.id:
            #         prop['position'] = 'end'
            #         prop['user'] = request.user.username
            #     else:
            #         prop['position'] = 'start'
            #         prop['user'] = User.objects.get(pk=prop['user_id']).username

            #     prop.pop("user_id")

            # data = json.dumps({'response': messages})
            return HttpResponse(data)

        except ObjectDoesNotExist:
            data = json.dumps({'response':'object does not exist'})
            return HttpResponse(data)

    def post(self, request):

        resp = json.loads(request.body)
        room = Room.objects.get(name=resp['dest'])
        
        message = Message()
        message.room = room
        message.sender = request.user
        message.text = resp['msg']

        message.save()
        
        # if resp['cat'] == 'User':
        #     dest = User.objects.get(username=resp['dest'])
        #     pc_id = list(PersonalChat.objects.filter(Q(user1__in=[request.user,dest]) & Q(user2__in=[dest,request.user])))

        #     if pc_id:
        #         self.store(pc_id[0], resp, request.user)
        #     else:
        #         pc = PersonalChat()
        #         pc.user1 = request.user
        #         pc.user2 = dest
        #         pc.save()
        #         self.store(pc, resp, request.user)
        
        # elif resp['cat'] == 'Group':
        #     dest = Group.objects.get(group_name=resp['dest'])
        #     message = Message()
        #     message.user_id = request.user
        #     message.text = resp['msg']
        #     message.group_id = dest
        #     message.save()

        return HttpResponse(JsonResponse(resp, safe=False))

    def store(self, pc, resp, user):
        message = Message()
        message.user_id = user
        message.text = resp["msg"]
        message.pc_id = pc
        message.save()