from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/$', views.index),
    url(r'^/show_users$', views.users),
    url(r'^/show_files$', views.files),
    url(r'^/show_reports$', views.reports),

]