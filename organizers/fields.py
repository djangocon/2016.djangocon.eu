from django.db import models
from django import forms


class TwitterifyFormField(forms.URLField):
    """
    Automatically replaces '@username' with the correct twitter URL.
    """
    def clean(self, value):
        if value is not None and value.startswith('@'):
            value = 'https://twitter.com/{}'.format(value[1:])
        return super(TwitterifyFormField, self).clean(value)


class TwitterifyModelField(models.URLField):
    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', TwitterifyFormField)
        return super(TwitterifyModelField, self).formfield(**kwargs)
