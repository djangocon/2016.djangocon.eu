from django.conf.urls import url
from django.contrib import admin

from .views import ScheduleView, ScheduleIcalView

urlpatterns = [
    url(r'^schedule/$', ScheduleView.as_view(), name='schedule'),
    url(r'^schedule/ical/$', ScheduleIcalView.as_view(), name='schedule_ical'),
]
