import logging

from webhooks.tito import TicketWebhookView


class TitoWebhookView(TicketWebhookView):
    def ticket_created(self, request):
        email = self.data['email']
        logging.info("New registration with email %s", email)
        return self.ok(request)
