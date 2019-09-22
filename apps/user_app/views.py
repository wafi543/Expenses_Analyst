from django.shortcuts import render, redirect, HttpResponse
from apps.user_app.models import *
import re
import bcrypt
from apps.user_app.core import *
from django.core.files.storage import FileSystemStorage
import datetime
import csv
import json
import requests
import os.path

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]{2,}')


def index(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        try:
            user = User.objects.get(id=uid)
            context = {
                'data': data,
                'user': user,
            }
        except:
            return HttpResponse('error loading user')

        if 'dashboard_errors' in request.session:
            context['errors'] = request.session['dashboard_errors']
        try:
            del request.session['dashboard_errors']
        except:
            print('error')
        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'login.html')


def logout(request):
    try:
        del request.session['uid']
    except:
        print('error')
    return redirect('/')


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

    if User.objects.filter(email=request.POST['email']).exists():
        user = User.objects.get(email=request.POST['email'])
        errors['email'] = 'Email is already exist'
        context['errors'] = errors

    if not 'errors' in context:
        pw_hash = bcrypt.hashpw(
            request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User.objects.create(
            first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        new_user.save()
        request.session['uid'] = new_user.id
        return redirect('/')
    else:
        uInfo = {
            'fname': request.POST['fname'],
            'lname': request.POST['lname'],
            'email': request.POST['email'],
        }
        context['uInfo'] = uInfo
        return render(request, 'register.html', context)


def login(request):
    errors = {}
    context = {}
    if User.objects.filter(email=request.POST['email']).exists():
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            print("password match")
            request.session['uid'] = user.id
            return redirect('/')
        else:
            uInfo = {
                'email': request.POST['email'],
            }
            errors['password'] = 'Password is invalid'
            context = {
                'errors': errors,
                'uInfo': uInfo,
            }
            print("failed password")
            return render(request, 'login.html', context)
    else:
        uInfo = {
            'email': request.POST['email'],
        }
        errors['email'] = 'Entered email is not registered'
        context = {
            'errors': errors,
            'uInfo': uInfo,
        }
        return render(request, 'login.html', context)


def profile(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        try:
            user = User.objects.get(id=uid)
            context = {
                'data': data,
                'user': user,
            }
        except:
            return HttpResponse('error loading user')
        return render(request, 'profile.html', context)
    else:
        redirect('/')


def update_profile(request):
    try:
        user = User.objects.get(id=request.POST['id'])
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
        if len(request.POST['password']) > 0:
            if len(request.POST['password']) < 8:
                errors['password'] = 'Your password must be at least 8 characters'
                context['errors'] = errors
            if request.POST['password'] != request.POST['confirm']:
                errors['confirm'] = 'Passwords does not match'
                context['errors'] = errors

        check = User.objects.get(email=request.POST['email'])
        print('id: '+str(check.id)+', post_id: '+request.POST['id'])
        if str(check.id) != request.POST['id']:
            errors['email'] = 'Email is already exist'
            context['errors'] = errors

        if not 'errors' in context:
            user.first_name = request.POST['fname']
            user.last_name = request.POST['lname']
            user.email = request.POST['email']
            if len(request.POST['password']) > 0:
                pw_hash = bcrypt.hashpw(
                    request.POST['password'].encode(), bcrypt.gensalt())
                user.password = pw_hash
            user.save()
            errors['done'] = 'Profile has been updated successfully'
            context['errors'] = errors
            context['user'] = user

            return render(request, 'profile.html', context)
        else:
            context['user'] = user
            return render(request, 'profile.html', context)
    except:
        HttpResponse('User id not found')


def add_file(request):
    return render(request, 'add_file.html')


def upload_file(request):
    errors = {}
    uid = str(request.session['uid'])
    time = datetime.datetime.now()
    time = str(time.strftime("%d_%m_%y_%H_%M_%S"))
    if request.method == "GET":
        print("a GET request is being made to this route")
        return redirect('/')
    if request.method == "POST":
        uploaded = request.FILES['document']
        fileName = uploaded.name
        fileSize = uploaded.size
        print(uploaded.name)
        print(uploaded.size)

        # check if size is less than 2.6 megabyte
        if(fileSize > 2621440):
            errors['file_size'] = "file size is too big"
            request.session['dashboard_errors'] = errors
            return redirect('/')
        if not fileName.endswith('.csv'):
            errors['file_type'] = "Uploaded file is not of type csv"
            request.session['dashboard_errors'] = errors
            return redirect('/')
        if request.POST['file_name'] == '':
            errors['file_name'] = 'File name is empty'
            request.session['dashboard_errors'] = errors
            return redirect('/')
        
        fileStore = FileSystemStorage()
        file_path = f"{uid}/{uid}_{time}.csv"
        fileStore.save(file_path, uploaded)
        user = User.objects.get(id=uid)
        new_file = File.objects.create(name=request.POST['file_name'], path=file_path, user=user)
        new_file.save()

    # send file to API
    f = open(f'apps/user_app/static/files/{file_path}', 'r')

    reader = csv.DictReader(f, fieldnames=("date", "type", "amount"))
    out = json.dumps([row for row in reader])

    print(out)

    r = requests.post('http://127.0.0.1:5000/', data=out)
    print(r.content)

    report_path = f"{uid}_{time}.json"
    # If the file name exists, write a JSON string into the file.
    # with open(f'apps/user_app/static/reports/{report_path}', 'w') as json_file:
    #     json.dump(r.text, json_file)
    # Save the JSON
    f = open( f'apps/user_app/static/reports/{report_path}', 'w')
    f.write(r.text)
    # Save report to the database
    new_report = Report.objects.create(
        name=request.POST['file_name'], path=report_path, user=user, file=new_file)
    new_report.save()

    errors['uploaded'] = 'File uploaded successfully'
    request.session['dashboard_errors'] = errors
    return redirect('/')


def my_files(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        try:
            user = User.objects.get(id=uid)
            files = File.objects.filter(user=user).order_by('id')
            context = {
                'data': data,
                'user': user,
                'files': files,
            }
        except:
            return HttpResponse('error loading user')
        return render(request, 'my_files.html', context)
    else:
        return render(request, 'login.html')

def contact(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        try:
            user = User.objects.get(id=uid)
            context = {
                'data': data,
                'user': user,
            }
        except:
            return HttpResponse('error loading user')
        return render(request, 'contact.html', context)
    else:
        return render(request, 'login.html')

def contact_process(request):
    errors = {}
    context = {'data':data}
    uid = str(request.session['uid'])
    time = datetime.datetime.now()
    time = str(time.strftime("%d_%m_%y_%H_%M_%S"))
    if request.method == "GET":
        print("a GET request is being made to this route")
        return redirect('/contact')
    if request.method == "POST":
        user = User.objects.get(id=uid)
        uploaded = request.FILES['document']
        fileName = uploaded.name
        fileSize = uploaded.size
        print(uploaded.name)
        print(uploaded.size)

        # check if size is less than 2.6 megabyte
        if(fileSize > 2621440):
            errors['file_size'] = "file size is too big"
            context['errors'] = errors
            return render(request, 'contact.html', context)
        if not fileName.endswith('.png') and not fileName.endswith('.jpg'):
            errors['file_type'] = 'Uploaded file is not an image'
            context['errors'] = errors
            return render(request, 'contact.html', context)
        fileStore = FileSystemStorage()
        path = f"messages/{uid}_{time}.png"
        fileStore.save(path, uploaded)
        new_message = Message.objects.create(content=request.POST['content'], path=path, sender=user)
        new_message.save()
        errors['uploaded'] = 'Your message has been sent successfully, we will review your message soon. Thank you!'
        context['errors'] = errors
        return render(request, 'contact.html', context)