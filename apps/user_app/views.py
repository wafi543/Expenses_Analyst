from django.shortcuts import render, redirect, session, HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('Hi')