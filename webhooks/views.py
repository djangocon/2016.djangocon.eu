import logging

from slacker import Error as SlackError

from webhooks.slack import get_connection as get_slack_connection, _convert_channels
from webhooks.tito import TicketWebhookView


logger = logging.getLogger(__name__)


def _get_channels_for_ticket(ticket):
    channels = ['#general', '#random']
    if 'donation' in ticket:
        return []  # Donations don't give access to the slack channel
    if 'speaker' in ticket:
        channels.append('#speakers')

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
        public_slack = get_slack_connection('djangoconeu-attendees')
        channels = _get_channels_for_ticket(self.data['release_title'].lower())
        channels = _convert_channels(public_slack, channels)
        if channels:
            try:
                public_slack.users.invite(
                    email=self.data['email'],
                    first_name=self.data['first_name'],
                    last_name=self.data['last_name'],
                    channels=channels,
                )
            except SlackError as e:
                if e.args[0] != 'already_invited':
                    raise

        return self.ok(request)
