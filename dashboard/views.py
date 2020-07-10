from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout
from network import Network

client = None
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        global client
        if client is None:
            client = Network(request.user.id)
            # start_new_thread(update_messages, ())

        context = {
            'title':'Dashboard',
            'count': range(20)
        }
        return render(request, 'test.html', context)

    return redirect('/auth')

def req(request):
    if request.method == 'POST':
        global client
        client.send_msg(request.POST['chat'])

        return HttpResponse(JsonResponse('message send!', safe=False))

    return redirect('/dashboard/')

def get_message(request):
    global client
    if client:
        if not client.msgs:
            return HttpResponse(JsonResponse('empty', safe=False))
        else:
            send = client.msgs.pop()
            return HttpResponse(JsonResponse(send, safe=False))

    return HttpResponse(JsonResponse('blom', safe=False))

# def update_messages():
#     global client, messages
#     try:
#         while True:
#             if client:
#                 new_messages = client.msgs
#                 messages.extend(new_messages)
#
#     except Exception as e:
#         print(e)


def Logout(request):
    global client
    if client:
        client.disconnect()
        client = None

    logout(request)
    return redirect('/')