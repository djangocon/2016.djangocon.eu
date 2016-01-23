from webhooks.tito import TicketWebhookView


class TitoWebhookView(TicketWebhookView):
    def ticket_created(self, request):
        pass  # TODO

    def ticket_updated(self, request):
        pass  # TODO

    def ticket_reassigned(self, request):
        pass  # TODO

    def ticket_unsnoozed(self, request):
        pass  # TODO

    def ticket_reassigned(self, request):
        pass  # TODO
