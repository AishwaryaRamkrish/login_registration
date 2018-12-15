from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^process_register$',views.process_register),
    url(r'^process_login$',views.process_login),
    url(r'^success$',views.success),
    url(r'^process_logout$',views.process_logout)
]