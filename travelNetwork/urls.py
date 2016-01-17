from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^client/', include('client.urls', namespace='client')),
    url(r'^api/', include('core.urls')),
)
