from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

def index(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        return HttpResponse('Hi')
    else:
        return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def registering(request):
    return HttpResponse('Soon...')


def login(request):
    return HttpResponse('Soon...')