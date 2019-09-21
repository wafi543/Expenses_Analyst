from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^registering$', views.registering),
    url(r'^add_file$', views.add_file),
    url(r'^logout$', views.logout),
]