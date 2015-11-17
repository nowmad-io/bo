from django.conf.urls import include, url
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'friends', views.UserViewSet)

urlpatterns = [

    url(r'^auth/', include('authentication.urls')),
    url(r'^index/$', views.index, name='index'),
    url(r'^reviews/$', views.ReviewList.as_view()),
    url(r'^reviews/(?P<pk>[0-9]+)/$', views.ReviewDetail.as_view()),
    url(r'^', include(router.urls), name='api-root'),
]
