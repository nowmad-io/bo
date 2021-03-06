from django.conf.urls import url
from friends.views import FriendViewSet, FriendshipRequestViewSet, FriendSearchViewSet

friends_list = FriendViewSet.as_view({
    'get': 'list'
})

friends_search = FriendSearchViewSet.as_view({
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

friendship_validation = FriendshipRequestViewSet.as_view({
    'get': 'accept'
})

friendship_rejection = FriendshipRequestViewSet.as_view({
    'get': 'reject'
})

friendship_cancel = FriendshipRequestViewSet.as_view({
    'get': 'cancel'
})

urlpatterns = ([
    url(r'^friends/$', friends_list, name='friends-list'),
    url(r'^friends/search/$', friends_search, name='friends-search'),
    url(r'^friendships/$', friendship_list, name='Friendship-incoming'),
    url(r'^friendships/incoming/$', friendship_incoming, name='Friendship-incoming'),
    url(r'^friendships/outgoing/$', friendship_outgoing, name='Friendship-outgoing'),
    url(r'^friendships/(?P<pk>[0-9]+)/$', friendship_details, name='Friendship-details'),
    url(r'^friendships/accept/(?P<pk>[0-9]+)/$', friendship_validation, name='Friendship-acceptation'),
    url(r'^friendships/reject/(?P<pk>[0-9]+)/$', friendship_rejection, name='Friendship-rejection'),
    url(r'^friendships/cancel/(?P<pk>[0-9]+)/$', friendship_cancel, name='Friendship-cancel')
])
