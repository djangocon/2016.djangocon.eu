from django.conf.urls import url

from faq.views import FAQListView

urlpatterns = [
    url(r'^$', FAQListView.as_view(), name='list'),
]
