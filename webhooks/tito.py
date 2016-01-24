import base64
import hmac
import json
import logging

from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic


class InvalidRequest(Exception):
    pass


def check_request(request):
    if 'Tito-Signature' not in request.META:
        logging.info("No signature head found")
        raise InvalidRequest("No signature header found")

    signature = requests.META['Tito-Signature']

    m = hmac.new(settings.TITO_SHARED_SECRET, msg=request.body, digestmod='sha256')
    encoded = base64.b64encode(m.digest())

    if not hmac.compare_digest(encoded, signature):
        logging.info("Signature %r does not match", signature)
        raise InvalidRequest("Signature does not match")


def clean_event_name(name):
    if not name:
        return ''
    name = name.strip()
    name = name.replace('.', '_')
    return name


class ValidWebhookMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            check_request(request)
        except InvalidRequest as e:
            raise PermissionDenied(e.msg)
        return super(ValidWebhookMixin, self).dispatch(request, *args, **kwargs)


class WebhookView(ValidWebhookMixin, generic.View):
    http_method_names = ['post']  # POST only
    hook_event_names = []

    def dispatch(self, request, *args, **kwargs):
        event = request.META.get('X-Webhook-Name')
        logging.info("Received raw tito even %r", event)
        event = clean_event_name(event)
        method = getattr(self, event, None)

        if not method or event not in self.hook_event_names:
            logging.info("Event %r not supported", event)
            return HttpResponseBadRequest("Webhook not supported")

        self.data = json.loads(request.body.decode('utf-8'))
        return method(request, *args, **kwargs)

    def ok(self, request, *args, **kwargs):
        """Return a 200 response"""
        return HttpResponse("Thanks Tito <3")


class TicketWebhookView(WebhookView):
    hook_event_names = {
        'ticket_created',
        'ticket_updated',
        'ticket_voided',
        'ticket_unsnoozed',
        'ticket_reassigned',
    }
