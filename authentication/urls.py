from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('djoser.urls.authtoken')),
]
