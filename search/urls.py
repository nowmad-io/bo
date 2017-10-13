from django.conf.urls import url
from search.views import SearchReviews

urlpatterns = ([
    url(r'^$', SearchReviews.as_view(), name='search'),
])
