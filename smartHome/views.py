from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import logging

from django.conf import settings

import loginApp.views

if not settings.DEBUG_:
    from . import switch
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522
    from . import led

# Create your views here.

logger = logging.getLogger(__name__)


@login_required(login_url='/recipes/login?next=/home/index/')
def homepage(request):
    if not settings.DEBUG_:
        switch.init()
        return render(request, "smartHome/index.html", context={"state": switch.get_switch_status()})
    else:
        return render(request, "smartHome/index.html", context={"DEBUG": True})


@csrf_protect
@login_required(login_url='/recipes/login?next=home/index/')
def ajax_switch(request):
    if request.is_ajax():
        switch.init()
        kapcsolo = request.POST.get('kapcsolo', '')
        allapot = request.POST.get('allapot', '')
        logger.debug("ajax switch method", "kapcsolo", kapcsolo, "allapot", allapot)
        if kapcsolo and allapot:
            return JsonResponse(switch.switch_toggle(kapcsolo, allapot))
    switch.clean()
    return JsonResponse({'error': 'nem talalhato a parameter'})


def rfid_login(request):
    if request.method == 'GET':
        reader = SimpleMFRC522()
        try:
            id, text = reader.read()
            text = text.strip()
            led.led_blink(1, led.GREEN)
            print("id: {}, text: {}".format(id, text))

        except Exception as e:
            print(e)
            led.led_blink(1, led.RED)
        finally:
            GPIO.cleanup()

