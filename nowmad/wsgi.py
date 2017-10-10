"""
WSGI config for nowmad project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
from socketio import Middleware

from sockets.views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nowmad.settings")

wsgi_application = get_wsgi_application()
application = Middleware(sio, DjangoWhiteNoise(wsgi_application)) 
