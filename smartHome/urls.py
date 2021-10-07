from django.urls import path

from . import views

app_name = 'smartHome'

urlpatterns = [
    path("index/", views.homepage, name='homepage'),
    path("ajax_switch/", views.ajax_switch, name='ajax_switch'),
    path("login_rfid/", views.rfid_login, name='rfid_login'),
]
