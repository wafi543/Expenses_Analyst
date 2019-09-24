from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from apps.user_app.models import User

# Create your views here.
def index(request):
    return render(request, 'dashboard.html')

def users(request):
    args= {'user': request.user_app_user}
    return render(request, 'show_users.html',args)

def files(request):
    return render(request, 'show_files.html')

def reports(request):
  #  args= {'user': request.User}
    return render(request, 'show_reports.html')