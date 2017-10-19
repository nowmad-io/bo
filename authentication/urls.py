from django.conf.urls import include, url
from .views import RegistrationView, MeView

urlpatterns = [
    url(r'^register/$', RegistrationView.as_view({'post': 'create'}), name='register'),
    url(r'^me/$', MeView.as_view({'get': 'retrieve'}), name='me'),
    url(r'^', include('djoser.urls.authtoken')),
]
