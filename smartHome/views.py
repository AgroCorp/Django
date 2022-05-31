from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import logging

from loginPage.wsgi import client1

# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='/recipes/login?next=/home/index/')
def homepage(request):
    leds = [1, 2, 3]
    return render(request, 'smartHome/index.html', {"leds": leds})


@csrf_protect
@login_required(login_url='/recipes/login?next=home/index/')
def ajax_switch(request):
    if request.is_ajax():
        led = request.POST.get('kapcsolo', None)
        state = request.POST.get('allapot', None)

        if led and state:

            ret = client1.publish("led_topic", f"{int(led)+1}_{state}")

            return JsonResponse({"status": bool(ret[1])})

    return JsonResponse({'error': 'nem talalhato a parameter'})
