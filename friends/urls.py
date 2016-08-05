from django.conf.urls import url, patterns
from friends.views import FriendViewSet, FriendshipEventViewset, FriendshipRequestViewSet

friends_list = FriendViewSet.as_view({
    'get': 'list'
})

friendship_list = FriendshipRequestViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

friendship_details = FriendshipRequestViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy',
    'put': 'update'
})

friendship_outgoing = FriendshipRequestViewSet.as_view({
    'get': 'outgoing_list'
})

friendship_incoming = FriendshipRequestViewSet.as_view({
    'get': 'incoming_list'
})

friendship_validation = FriendshipEventViewset.as_view({
    'post': 'accept'
})

friendship_rejection = FriendshipEventViewset.as_view({
    'post': 'reject'
})



urlpatterns = ([
    url(r'^friends/$', friends_list, name='friends-list'),
    url(r'^friendships/$', friendship_list, name='Friendship-incoming'),
    url(r'^friendships/incoming/$', friendship_incoming, name='Friendship-incoming'),
    url(r'^friendships/outgoing/$', friendship_outgoing, name='Friendship-outgoing'),
    url(r'^friendships/(?P<pk>[0-9]+)/$', friendship_details, name='Friendship-details'),
    url(r'^friendships/accept/(?P<pk>[0-9]+)/$', friendship_validation, name='Friendship-acceptation'),
    url(r'^friendships/reject/(?P<pk>[0-9]+)/$', friendship_rejection, name='Friendship-rejection')
])
