from django.conf.urls import url
from django.contrib import admin

from .views import IndexView, ArticleView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^article/(?P<slug>[-\w]+)/$', ArticleView.as_view(), name='article'),
]
