from django.conf.urls import url
from django.contrib import admin

from .views import ListView, DetailView, BulkUploadView, ScheduleView, ScheduleIcalView

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'^(?P<pk>[\d]+)$', DetailView.as_view(), name='detail'),
    url(r'^upload/$', BulkUploadView.as_view(), name='upload'),
    url(r'^schedule/$', ScheduleView.as_view(), name='schedule'),
    url(r'^schedule/ical/$', ScheduleIcalView.as_view(), name='schedule_ical'),
]
