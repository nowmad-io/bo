# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed
async_mode = None

import os

from django.http import HttpResponse
from rest_framework.authtoken.models import Token
import socketio

sio = socketio.Server(async_mode=async_mode)
namespace = '/sockets'

def FriendAccept(user, friend, serialiser_user ,serializer_friend):
    sio.emit('friend.new', {'friend': serializer_friend}, room=user.sid, namespace=namespace)
    sio.emit('friend.new', {'friend': serialiser_user}, room=friend.sid, namespace=namespace)

def FriendCreate(users, request):
    for user in users:
        sid = user.sid
        sio.emit('friend.create', {'request': request}, room=sid, namespace=namespace)

def FriendReject(users, request):
    for user in users:
        sid = user.sid
        sio.emit('friend.reject', {'request': request}, room=sid, namespace=namespace)

@sio.on('authenticate', namespace=namespace)
def authenticate(sid, message):
    user = Token.objects.get(key=message['token']).user
    user.sid = sid
    user.save();

@sio.on('connect', namespace=namespace)
def connect(sid, environ):
    sio.emit('connected', {}, room=sid, namespace=namespace)


@sio.on('disconnect', namespace=namespace)
def disconnect(sid):
    sio.disconnect(sid, namespace=namespace)
