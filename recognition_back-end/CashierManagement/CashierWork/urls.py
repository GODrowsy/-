from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'CashierWork'
urlpatterns = [
    url(r'^find', views.find),
    url(r'^Findall', views.findall),
    url(r'^wxAdSign', views.wxAdSign),
    url(r'^wxCaSign', views.wxCaSign),
]