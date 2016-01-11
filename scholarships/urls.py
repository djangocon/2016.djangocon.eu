from django.conf.urls import url
from django.contrib import admin

from scholarships.views import LandingView, CreateView, ThankYouView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^apply/$', CreateView.as_view(), name='apply'),
    url(r'^thanks/$', ThankYouView.as_view(), name='thanks'),
]
