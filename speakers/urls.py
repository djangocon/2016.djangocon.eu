from django.conf.urls import url
from django.shortcuts import redirect

from .views import ListView, DetailView, BulkUploadView

def permanent_redirect(*args, **kwargs):
    kwargs['permanent'] = True
    def view(request):
        return redirect(*args, **kwargs)

    return view

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'^(?P<pk>[\d]+)$', DetailView.as_view(), name='detail'),
    url(r'^upload/$', BulkUploadView.as_view(), name='upload'),

    # Old URLs
    url(r'^schedule/$', permanent_redirect('schedule:schedule')),
    url(r'^schedule/ical/$', permanent_redirect('schedule:ical')),
]
