from django.apps import AppConfig

from . import slack


class WebhooksConfig(AppConfig):
    name = 'webhooks'

    def ready(self):
        slack._monkeypatch_user_invite()
