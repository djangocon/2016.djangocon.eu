from django.conf.urls import url

from badge.views import badge

urlpatterns = [
    url(r'^$', badge, name='badge'),
]
