from django.shortcuts import render, redirect, HttpResponse
from apps.user_app.models import *
import re
import bcrypt
# Create your views here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]{2,}')


def index(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        return HttpResponse('success logged in, your id is: '+str(request.session['uid']))
    else:
        print('sdf')
        return render(request, 'login.html')


def register(request):
    if 'uid' in request.session:
        return redirect('/')
    else:
        return render(request, 'register.html')


def registering(request):
    context = {}
    errors = {}
    if not NAME_REGEX.match(request.POST['fname']):
        errors['fname'] = 'First name must contain at least two letters and contains only letters'
        context['errors'] = errors
    if not NAME_REGEX.match(request.POST['lname']):
        errors['lname'] = 'Last name must contain at least two letters and contains only letters'
        context['errors'] = errors
    if not EMAIL_REGEX.match(request.POST['email']):
        errors['email'] = 'Invalid email address'
        context['errors'] = errors
    if len(request.POST['password']) < 8:
        errors['password'] = 'Your password must be at least 8 characters'
        context['errors'] = errors
    if request.POST['password'] != request.POST['confirm']:
        errors['confirm'] = 'Passwords does not match'
        context['errors'] = errors

    try:
        user = User.objects.get(email=request.POST['email'])
        errors['email'] = 'Email is already exist'
        context['errors'] = errors
    except:
        print('Email is not found')

    if not 'errors' in context:
        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(
            first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        new_user.save()
        request.session['uid'] = new_user.id
        return redirect('/')
    else:
        uInfo ={
            'fname': request.POST['fname'],
            'lname': request.POST['lname'],
            'email': request.POST['email'],
        }
        context['uInfo'] = uInfo
        return render(request, 'register.html', context)

    return HttpResponse('Soon...')


def login(request):
    errors = {}
    context = {}
    try:
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("password match")
            request.session['uid'] = user.id
            return redirect('/')
        else:
            errors['password'] = 'Password is invalid'
            context = {
                'errors': errors
            }
            print("failed password")
            return render(request, 'login.html', context)
    except:
        uInfo = {
            'email': request.POST['email'],
        }
        errors['email'] = 'Entered email is not registered'
        context = {
            'errors': errors,
            'uInfo': uInfo,
        }
        return render(request, 'login.html', context)


def add_file(request):
    return render(request, 'add_file.html')

def logout(request):
    del request.session['uid']
    return redirect('/')

