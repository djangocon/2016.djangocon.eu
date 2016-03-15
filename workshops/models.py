from django.core.urlresolvers import reverse
from django.db import models

from schedule.models import AbstractEvent


class Workshop(AbstractEvent):
    location = 'MÜSZI'

    def get_absolute_url(self):
        return reverse('workshops:detail', args=[self.pk])
