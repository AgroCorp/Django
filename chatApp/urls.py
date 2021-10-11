from django.urls import path

from . import views

app_name = 'chatApp'

urlpatterns = [
    path("", views.homepage, name='homepage'),
    path('create_room', views.create_room, name='create_room'),
    path('join_room', views.join_room, name='join_room'),
    path('exit_room', views.exit_room, name='exit_room'),

]
