"""
WSGI config for loginPage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import paho.mqtt.client as paho
from loginPage import settings

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginPage.settings')

application = get_wsgi_application()


def on_publish(client, userdata, result):
    print("data published")


client1 = paho.Client("controller")
client1.on_publish = on_publish
client1.connect(settings.BROKER, settings.BROKER_PORT)


