from slacker import Slacker, Users

from django.conf import settings


def _invite(self, email, **kwargs):
    """
    There's only a private API to invite users to a slack team.
    This function will be monkeypatched onto slacker.User and it seems to work.
    """
    data = dict(email=email, **kwargs)
    if 'channels' in data and not isinstance(data['channels'], str):
        data['channels'] = ','.join(data['channels'])
    data['_attempts'] = 1  # required by slack for some reason
    return self.post('users.admin.invite', data=data)


def _monkeypatch_user_invite():
    Users.invite = _invite


def get_connection(slack_name):
    token = settings.SLACK_API_TOKENS[slack_name]
    return Slacker(token)


def get_user_emails(slack_team):
    response = slack_team.users.list()
    assert response.successful
    return {user['profile']['email'] for user in response.body['members']}
