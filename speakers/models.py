import requests

from django.core.files import File
from django.db import models
from django.utils import timezone


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    picture = models.ImageField()
    twitter = models.CharField(max_length=50, blank=True)
    github = models.CharField(max_length=50, blank=True)
    talk_title = models.CharField(max_length=200)
    talk_description = models.TextField()
    published = models.BooleanField(default=False)

    is_keynote = models.BooleanField(default=False)

    def __str__(self):
        return self.name
