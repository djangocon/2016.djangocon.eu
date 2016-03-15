from django.db import models

from schedule.models import AbstractEvent


class Workshop(AbstractEvent):
    location = 'MÜSZI'
