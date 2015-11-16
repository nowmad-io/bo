from django.conf.urls import include, url
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [

    url(r'^auth/', include('authentication.urls')),
    url(r'^index/$', views.index, name='index'),
    url(r'^', include(router.urls), name='api-root'),
]
