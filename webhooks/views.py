import logging

from webhooks.slack import get_connection as get_slack_connection, get_user_emails
from webhooks.tito import TicketWebhookView


logger = logging.getLogger(__name__)


def _get_channels_for_ticket(ticket):
    channels = ['#general', '#random']
    if 'donation' in ticket:
        return []  # Donations don't give access to the slack channel
    if 'speaker' in ticket:
        channels.append('#speakers')
    if 'scholarship ticket' in ticket:
        channels.append('#scholars')

    return channels


class TitoWebhookView(TicketWebhookView):
    def ticket_completed(self, request):
        email = self.data['email']
        logger.info("New registration with email %s", email)

        # Post message to internal slack notification channel
        internal_slack = get_slack_connection('djangoconeu')
        internal_slack.chat.post_message(
            channel='#notifications',
            text="%(name)s registered a %(release_title)s (reference: %(reference)s) :tada:" % self.data,
            username="titobot",
            icon_emoji=":ticket:",
        )

        # Invite to public slack
        channels = _get_channels_for_ticket(self.data['release_title'].lower())
        if channels:
            public_slack = get_slack_connection('djangoconeu-attendees')
            existing_users = get_user_emails(public_slack)
            if email not in existing_users:
                public_slack.users.invite(
                    email=self.data['email'],
                    first_name=self.data['first_name'],
                    last_name=self.data['last_name'],
                    channels=channels,
                )

        return self.ok(request)
