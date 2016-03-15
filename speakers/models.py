from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import urlencode
from django.utils.html import format_html

from djangocon.toolbox import Action

from schedule.models import AbstractEvent
from schedule.models import get_talk_default_date, get_talk_default_start  # required for old migrations


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


class Talk(AbstractEvent):
    speaker = models.OneToOneField('Speaker', blank=True, null=True)

    location = 'Budapest Music Center'

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
    def css_class(self):
        if not self.speaker:
            return 'not-talk'
        speaker = self.speaker
        if speaker.is_keynote:
            return 'talk keynote'
        return 'talk'
