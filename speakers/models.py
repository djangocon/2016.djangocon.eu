from datetime import date, datetime, time

import icalendar

from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import urlencode
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone

from djangocon.toolbox import Action


FIRST_CONFERENCE_DAY = date(2016, 3, 30)


def get_talk_default_date():
    last_talk = Talk.objects.last()
    if last_talk is None:
        return FIRST_CONFERENCE_DAY
    return last_talk.day


def get_talk_default_start():
    last_talk = Talk.objects.last()
    if last_talk is None:
        return None
    return last_talk.end


def us_friendly_html_timeslot(t):
    if t < time(13, 0, 0):
        return '{time:%H}:{time:%M}'.format(time=t)
    return '<span class="ustime" title="{time:%I}:{time:%M}{time:%p}">{time:%H}:{time:%M}</span>'.format(time=t)


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    picture = models.ImageField()
    twitter = models.CharField(max_length=50, blank=True, help_text="Don't include any leading @")
    github = models.CharField(max_length=50, blank=True)
    talk_title = models.CharField(max_length=200)
    talk_description = models.TextField()
    mentoring = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    is_keynote = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_picture_html(self, size=285):
        if self.picture:
            src = self.picture.url
        else:
            src = 'http://api.adorable.io/avatars/%s/%s' % (size, urlencode(self.name))

        return format_html('<img alt="{name}" src="{src}" class="speakerpicture">', name=self.name, src=src)

    def get_absolute_url(self):
        return reverse('speakers:detail', args=[self.pk])

    @property
    def twitter_url(self):
        return 'https://twitter.com/%s' % self.twitter

    @property
    def github_url(self):
        return 'https://github.com/%s' % self.github

    @property
    def url(self):
        if self.twitter:
            return self.twitter_url
        if self.github:
            return self.github_url
        return self.get_absolute_url()

    def get_toolbox(self, user):
        if user.is_staff:
            yield Action(reverse('admin:speakers_speaker_change', args=[self.pk]), 'Edit in admin', 'pencil')


class TalkQuerySet(models.QuerySet):
    def as_ical(self, **kwargs):
        calendar = icalendar.Calendar()
        for k, v in kwargs.items():
            calendar[k] = v
        for talk in self:
            calendar.add_component(talk.as_ical())
        return calendar


class Talk(models.Model):
    day = models.DateField(default=get_talk_default_date)
    start = models.TimeField(default=get_talk_default_start)
    end = models.TimeField()
    speaker = models.OneToOneField('Speaker', blank=True, null=True)
    _description = models.TextField(blank=True)

    objects = TalkQuerySet.as_manager()

    class Meta:
        ordering = ('day', 'start')

    def get_absolute_url(self):
        if not self.speaker:
            return None
        return self.speaker.get_absolute_url()

    @property
    def author(self):
        if not self.speaker:
            return None
        return self.speaker.name

    @property
    def title(self):
        if not self.speaker:
            return self._description
        return self.speaker.talk_title

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
    def css_class(self):
        if not self.speaker:
            return 'not-talk'
        speaker = self.speaker
        if speaker.is_keynote:
            return 'talk keynote'
        return 'talk'

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
        return "talk{}@2016.djangocon.eu".format(self.pk)

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
