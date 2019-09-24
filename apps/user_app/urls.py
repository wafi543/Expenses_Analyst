from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^registering$', views.registering),
    url(r'^/admin_dashboard$', views.index_admin),
    url(r'^admin_dashboard/show_users$', views.users),
    url(r'^admin_dashboard/show_files$', views.files),
    url(r'^admin_dashboard/show_reports$', views.reports),
]