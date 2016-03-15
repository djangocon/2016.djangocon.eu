from datetime import date, datetime, time

import icalendar

from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone


FIRST_CONFERENCE_DAY = date(2016, 3, 30)


def get_talk_default_date():
    return FIRST_CONFERENCE_DAY


def get_talk_default_start():
    return time(10, 0, 0)


def us_friendly_html_timeslot(t):
    if t < time(13, 0, 0):
        return '{time:%H}:{time:%M}'.format(time=t)
    return '<span class="ustime" title="{time:%I}:{time:%M}{time:%p}">{time:%H}:{time:%M}</span>'.format(time=t)




class EventQuerySet(models.QuerySet):
    def as_ical(self, **kwargs):
        calendar = icalendar.Calendar()
        for k, v in kwargs.items():
            calendar[k] = v
        for event in self:
            calendar.add_component(event.as_ical())
        return calendar


class AbstractEvent(models.Model):
    day = models.DateField(default=get_talk_default_date)
    start = models.TimeField(default=get_talk_default_start)
    end = models.TimeField()

    _title = models.CharField(max_length=200, blank=True)
    _description = models.TextField(blank=True)
    _author = models.CharField(max_length=200, blank=True)

    objects = EventQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ('day', 'start')

    def get_absolute_url(self):
        return None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def title_html(self):
        title, url = self.title, self.get_absolute_url()
        if not url:
            return title
        return format_html('<a href="{}">{}</a>', url, title)

    @property
    def time_slot(self):
        return '{start:%H}:{start:%M} - {end:%H}:{end:%M}'.format(start=self.start, end=self.end)

    @property
    def time_slot_html(self):
        """
        A US-friendlier time-slot display
        """
        return mark_safe('{} - {}'.format(
            us_friendly_html_timeslot(self.start),
            us_friendly_html_timeslot(self.end),
        ))

    @property
    def weekday(self):
        return self.day.strftime('%A')

    @property
    def dt_start(self):
        return timezone.make_aware(datetime.combine(self.day, self.start))

    @property
    def dt_end(self):
        return timezone.make_aware(datetime.combine(self.day, self.end))

    @property
    def ical_uid(self):
        app, model = self._meta.label_lower.split('.')
        return "{}{}@2016.djangocon.eu".format(model, self.pk)

    @property
    def ical_summary(self):
        if not self.author:
            return self.title
        return '{} - {}'.format(self.author, self.title)

    def as_ical(self):
        """
        Return a representation of the current talk as an icalendar.Event.
        """
        event = icalendar.Event()
        event.add("dtstart", self.dt_start)
        event.add("dtend", self.dt_end)
        event.add("uid", self.ical_uid)
        event.add("summary", self.ical_summary)
        event.add("location", "Budapest Music Center, Budapest, Hungary")
        return event
