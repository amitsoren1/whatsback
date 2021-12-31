"""
WSGI config for chatback project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import socketio

from django.core.wsgi import get_wsgi_application
from .socketio import sio
# sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatback.settings')

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application, static_files={
    '/static': '/app/chatback/static',
    '/media': '/app/chatback/media',
})

# import eventlet
# import eventlet.wsgi

# eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
