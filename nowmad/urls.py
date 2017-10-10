from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'', include('sockets.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('core.urls')),
]
