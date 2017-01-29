from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_appointment$', views.create_appointment, name='create_appointment'),
    url(r'^view_appointment/(?P<appointment_id>\d+)$', views.view_appointment, name='view_appointment'),
    url(r'^update_appointment/(?P<appointment_id>\d+)$', views.update_appointment, name='update_appointment'),
    url(r'^delete_appointment/(?P<appointment_id>\d+)$', views.delete_appointment, name='delete_appointment'),
    url(r'^display_add_appointment$', views.display_add_appointment, name='display_add_appointment'),
]
