from django.core.management.commands.runserver import Command as RunCommand
from django.conf import settings

from sockets.views import sio

class Command(RunCommand):
    help = 'Run the Socket.IO server'

    def handle(self, *args, **options):
        if sio.async_mode == 'threading':
            print('-------threading------')
            super(Command, self).handle(*args, **options)
        elif sio.async_mode == 'eventlet':
            print('-------eventlet------')
            # deploy with eventlet
            import eventlet
            import eventlet.wsgi
            from nowmad.wsgi import application
            eventlet.wsgi.server(eventlet.listen(('', settings.DEFAULT_PORT)), application)
        elif sio.async_mode == 'gevent':
            print('-------gevent------')
            # deploy with gevent
            from gevent import pywsgi
            from nowmad.wsgi import application
            try:
                from geventwebsocket.handler import WebSocketHandler
                websocket = True
            except ImportError:
                websocket = False
            if websocket:
                pywsgi.WSGIServer(
                    ('', settings.DEFAULT_PORT), application,
                    handler_class=WebSocketHandler).serve_forever()
            else:
                pywsgi.WSGIServer(('', settings.DEFAULT_PORT), application).serve_forever()
        elif sio.async_mode == 'gevent_uwsgi':
            print('-------gevent_uwsgi------')
            print('Start the application through the uwsgi server. Example:')
            print('uwsgi --http :5000 --gevent 1000 --http-websockets '
                  '--master --wsgi-file nowmad/wsgi.py --callable '
                  'application')
        else:
            print('-------Unknown------')
            print('Unknown async_mode: ' + sio.async_mode)
