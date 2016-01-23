from django.conf.urls import url

from .views import TitoWebhookView

def debugview(request):
    """
    A temporary view to debug webhooks. Works by triggering an exception
    which will bubble up and use Django's built-in error reporting, emailing
    a description of the request to the site admins.
    """
    raise Exception("Boom")

urlpatterns = [
    url(r'^tito/$', debugview),  # XXX: Remove later
    url(r'^tito/$', TitoWebhookView.as_view(), name='tito'),
]
