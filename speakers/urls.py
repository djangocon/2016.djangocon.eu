from django.conf.urls import url
from django.contrib import admin

from .views import ListView, BulkUploadView

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'^upload/$', BulkUploadView.as_view(), name='upload'),
]
