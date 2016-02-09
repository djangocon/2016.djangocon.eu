from django.conf.urls import url
from django.contrib import admin

from cfp.views import LandingView, CreateView, ThankYouView, ProposalDownloadView, ProposeWorkshopView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^propose/$', CreateView.as_view(), name='propose'),
    url(r'^workshop/$', ProposeWorkshopView.as_view(), name='workshop'),
    url(r'^thanks/$', ThankYouView.as_view(), name='thanks'),
    url(r'^download/$', ProposalDownloadView.as_view(), name='download'),
]
