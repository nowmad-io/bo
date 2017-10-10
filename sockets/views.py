# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import os

from django.http import HttpResponse
import socketio

basedir = os.path.dirname(os.path.realpath(__file__))
sio = socketio.Server(async_mode=async_mode)
thread = None
namespace = '/sockets'

def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my response', {'data': 'Server generated event'},
                 namespace=namespace)


@sio.on('my event', namespace=namespace)
def test_message(sid, message):
    sio.emit('my response', {'data': message['data']}, room=sid,
             namespace=namespace)


@sio.on('my broadcast event', namespace=namespace)
def test_broadcast_message(sid, message):
    sio.emit('my response', {'data': message['data']}, namespace=namespace)


@sio.on('join', namespace=namespace)
def join(sid, message):
    sio.enter_room(sid, message['room'], namespace=namespace)
    sio.emit('my response', {'data': 'Entered room: ' + message['room']},
             room=sid, namespace=namespace)


@sio.on('leave', namespace=namespace)
def leave(sid, message):
    sio.leave_room(sid, message['room'], namespace=namespace)
    sio.emit('my response', {'data': 'Left room: ' + message['room']},
             room=sid, namespace=namespace)


@sio.on('close room', namespace=namespace)
def close(sid, message):
    sio.emit('my response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'], namespace=namespace)
    sio.close_room(message['room'], namespace=namespace)


@sio.on('my room event', namespace=namespace)
def send_room_message(sid, message):
    sio.emit('my response', {'data': message['data']}, room=message['room'],
             namespace=namespace)


@sio.on('disconnect request', namespace=namespace)
def disconnect_request(sid):
    sio.disconnect(sid, namespace=namespace)


@sio.on('connect', namespace=namespace)
def test_connect(sid, environ):
    print('yooo', sid)
    sio.emit('my response', {'data': 'Connected', 'count': 0}, room=sid,
             namespace=namespace)


@sio.on('disconnect', namespace=namespace)
def test_disconnect(sid):
    print('Client disconnected')
