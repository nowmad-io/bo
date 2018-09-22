from django.conf.urls import include, url
from rest_framework import routers

from core.views import ReviewViewSet, CategoryViewSet, PlaceListView, ReviewPicturesViewSet, NotifyMe

router = routers.DefaultRouter()
router.register(r'reviews', ReviewViewSet, 'reviews')
router.register(r'categories', CategoryViewSet, 'categories')

urlpatterns = [
    url(r'^notifyme/$', NotifyMe.as_view()),
    url(r'^places/$', PlaceListView.as_view(), name='placesList'),
    url(r'^reviews/(?P<pk>[a-zA-Z0-9]+)/pictures/$', ReviewPicturesViewSet.as_view({'put': 'update'}), name='Review-pictures'),
    url(r'^auth/', include('authentication.urls')),
    url(r'^', include(router.urls), name='api-root'),
    url(r'^', include('friends.urls'), name='friends')
]
