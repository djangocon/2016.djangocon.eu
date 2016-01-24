import base64
import hmac
import json
import logging

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic

logger = logging.getLogger(__name__)


class InvalidRequest(Exception):
    pass


def check_request(request):
    try:
        signature = request.META['HTTP_TITO_SIGNATURE'].encode('ascii')
    except KeyError:
        logger.error("No signature header found")
        raise InvalidRequest("No signature header found")
    except UnicodeEncodeError:
        logger.error("Invalid non-ascii signature found")
        raise InvalidRequest("Invalid non-ascii signature found")

    m = hmac.new(settings.TITO_SHARED_SECRET, msg=request.body, digestmod='sha256')
    encoded = base64.b64encode(m.digest())

    if not hmac.compare_digest(encoded, signature):
        logger.error("Signature %r does not match", signature)
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
            return self.invalid_signature(e)
        return self.valid_signature(request, *args, **kwargs)

    def invalid_signature(self, error):
        raise PermissionDenied(error.args[0]) from error


class WebhookView(ValidWebhookMixin, generic.View):
    http_method_names = ['post']  # POST only
    hook_event_names = []

    def valid_signature(self, request, *args, **kwargs):
        event = request.META.get('HTTP_X_WEBHOOK_NAME')
        logger.info("Received raw tito even %r", event)
        event = clean_event_name(event)
        method = getattr(self, event, None)

        if not method or event not in self.hook_event_names:
            logger.error("Event %r not supported", event)
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
        'ticket_completed',
        'ticket_voided',
        'ticket_unsnoozed',
        'ticket_reassigned',
    }
