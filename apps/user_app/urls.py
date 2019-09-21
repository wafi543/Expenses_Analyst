from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^registering$', views.registering),
    url(r'^profile$', views.profile),
    url(r'^update_profile$', views.update_profile),
]