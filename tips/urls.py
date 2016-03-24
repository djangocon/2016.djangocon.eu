from django.conf.urls import url

from .views import index, airport, money

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^airport/$', airport, name='airport'),
    url(r'^money/$', airport, name='money'),
]
