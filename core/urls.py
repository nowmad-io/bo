from django.conf.urls import include, url
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls), name='api-root'),
    url(r'^index/$', views.index, name='index'),
]
