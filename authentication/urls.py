from django.conf.urls import include, url
from .views import RegistrationView

urlpatterns = [
    url(r'^register/$', RegistrationView.as_view({'post': 'create'}), name='register'),
    url(r'^', include('djoser.urls.authtoken')),
]
