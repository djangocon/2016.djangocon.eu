from django.conf.urls import url

from .views import ScheduleView, IcalScheduleView

urlpatterns = [
    url(r'^$', ScheduleView.as_view(), name='schedule'),
    url(r'^ical/$', IcalScheduleView.as_view(), name='ical'),
]
