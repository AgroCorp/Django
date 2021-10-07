from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random

chatrooms = {}

# Create your views here.


@login_required(login_url='/recipes/login?next=/chat/')
def homepage(request):
    return render(request, 'chatApp/home.html')


@login_required(login_url='/recipes/login?next=/chat/')
def create_room(request):
    if request.method == 'GET':
        room_id = random.randint(1000, 9999)
        while room_id in chatrooms.keys():
            room_id = random.randint(1000, 9999)
        chatrooms[room_id] = 1

        print("A szoba azonositoja", room_id)
        return render(request, 'chatApp/room.html', {"room_id": room_id})

    return render(request, 'chatApp/home.html', {"error": 'Valami hiba tortent a szoba letrehozasanal!'})


@login_required(login_url='/recipes/login?next=/chat/')
def join_room(request):
    if request.method == 'POST':
        join_code = request.POST.get('joinCode', None)

        if join_code:
            return render(request, 'chatApp/room.html', {'room_id': join_code})


def exit_room(request):
    return render(request, 'chatApp/home.html', {})


