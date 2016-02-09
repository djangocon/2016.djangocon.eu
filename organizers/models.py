from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import urlencode
from django.utils.html import format_html
from django.utils.text import slugify

from djangocon.toolbox import Action

from .fields import TwitterifyModelField


class OrganizerQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)


class Organizer(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    url = TwitterifyModelField(blank=True, help_text="Use @username as a twitter shortcut")
    emoji = models.CharField(max_length=10, blank=True)
    picture = models.ImageField(blank=True)
    published = models.BooleanField(default=False)

    objects = OrganizerQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_picture_html(self, size=285):
        if self.picture:
            src = self.picture.url
        else:
            src = 'http://api.adorable.io/avatars/%s/%s' % (size, urlencode(self.name))

        return format_html('<img alt="{name}" src="{src}">', name=self.name, src=src)

    def get_toolbox(self, user):
        if user.is_staff:
            yield Action(reverse('admin:organizers_organizer_change', args=[self.pk]), 'Edit in admin', 'pencil')

    @property
    def data_emoji_alt(self):
        if not self.emoji:
            return ''
        return format_html('data-emoji-alt="{}"', self.emoji)

    def get_absolute_url(self):
        return reverse('organizers:list') + '#{}'.format(self.slug)

    @property
    def slug(self):
        return slugify(self.name)
