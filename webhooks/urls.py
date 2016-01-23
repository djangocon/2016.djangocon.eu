from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import TitoWebhookView

urlpatterns = [
    url(r'^tito/$', csrf_exempt(TitoWebhookView.as_view()), name='tito'),
]
