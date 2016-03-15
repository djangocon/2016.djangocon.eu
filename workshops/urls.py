from django.conf.urls import url

from .views import DetailView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(), name='detail'),
]
