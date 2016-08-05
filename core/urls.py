from django.conf.urls import include, url
from core.views import ReviewViewSet, UserViewSet, index
from friends.views import FriendViewSet, FriendshipRequestViewSet


from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet, 'reviews')


urlpatterns = [
    url(r'^auth/', include('authentication.urls')),
    url(r'^index/$', index, name='index'),
    url(r'^', include(router.urls), name='api-root'),
    url(r'^', include('friends.urls'), name='friends')
]
