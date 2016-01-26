from django.conf.urls import url
from django.contrib import admin

from scholarships.views import LandingView, ThankYouView, ApplicationsDownloadView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^thanks/$', ThankYouView.as_view(), name='thanks'),
    url(r'^download/$', ApplicationsDownloadView.as_view(), name='download'),
]
