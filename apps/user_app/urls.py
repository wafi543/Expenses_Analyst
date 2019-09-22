from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^registering$', views.registering),
    url(r'^profile$', views.profile),
    url(r'^update_profile$', views.update_profile),
    url(r'^add_file$', views.add_file),
    url(r'^upload_file$', views.upload_file),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)