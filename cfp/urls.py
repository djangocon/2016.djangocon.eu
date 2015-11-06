from django.conf.urls import url
from django.contrib import admin

from cfp.views import CreateView, ThankYouView

urlpatterns = [
    url(r'^$', CreateView.as_view(), name='propose'),
    url(r'^thanks/$', ThankYouView.as_view(), name='thanks'),
]
