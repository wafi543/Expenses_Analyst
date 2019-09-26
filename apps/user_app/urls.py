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
    url(r'^admin_dashboard$', views.index_admin),
    url(r'^admin_dashboard/show_users$', views.users),
    url(r'^admin_dashboard/show_files$', views.files),
    #url(r'^admin_dashboard/show_files/(?P<id>[0-9]+)/(?P<user_id>[0-9]+)/delete$', views.admin_delete_file),
    url(r'^admin_dashboard/show_reports$', views.reports),
    url(r'^admin_dashboard/(?P<id>[0-9]+)/delete$', views.delete_user),
    url(r'^admin_dashboard/show_messages$', views.show_messages),
    url(r'^admin_dashboard/(?P<id>[0-9]+)/admin_profile$', views.admin_profile),
    url(r'^admin_dashboard/(?P<id>[0-9]+)/admin_update_profile$', views.admin_update_profile),
    url(r'^admin_dashboard/(?P<id>[0-9]+)/show_message$', views.show_message),
    url(r'^profile$', views.profile),
    url(r'^update_profile$', views.update_profile),
    url(r'^upload_file$', views.upload_file),
    url(r'^my_files$', views.my_files),
    url(r'^my_files/(?P<id>[0-9]+)/view$', views.view_file),
    url(r'^my_files/(?P<id>[0-9]+)/delete$', views.delete_file),
    url(r'^contact$', views.contact),
    url(r'^contact_process$', views.contact_process),
    url(r'^my_reports$', views.my_reports),
    url(r'^my_reports/(?P<id>[0-9]+)/view$', views.view_report),
    url(r'^my_reports/(?P<id>[0-9]+)/delete$', views.delete_report),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
