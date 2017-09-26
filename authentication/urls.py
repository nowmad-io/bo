from django.conf.urls import include, url
from . import views


urlpatterns = [
    # url(r'^register/$', views.RegistrationView.as_view(), name='register'),
    url(r'^', include('djoser.urls.authtoken')),
]
