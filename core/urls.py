from django.conf.urls import include, url
from rest_framework import routers

from core.views import ReviewViewSet, UserViewSet, index, CategoryViewSet
from friends.views import FriendViewSet, FriendshipRequestViewSet

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet, 'reviews')
router.register(r'categories', CategoryViewSet, 'categories')

urlpatterns = [
    url(r'^search/', include('search.urls')),
    url(r'^auth/', include('authentication.urls')),
    url(r'^index/$', index, name='index'),
    url(r'^', include(router.urls), name='api-root'),
    url(r'^', include('friends.urls'), name='friends')
]
