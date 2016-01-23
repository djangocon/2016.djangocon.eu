from glob import glob
import os

import markdown as md

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property


def _get_markdown_content(slug):
    """
    Try and locate a post file given its slug. Raise PostDoesNotExist if file
    not found
    """
    filename = '%s.md' % slug
    fullpath = os.path.join(settings.TINYBLOG_ROOT_DIR, filename)
    try:
        with open(fullpath) as f:
            return f.read()
    except OSError as error:
        raise PostDoesNotExist from error


class PostDoesNotExist(ObjectDoesNotExist):
    pass


class PostManager(object):
    def __init__(self, model=None):
        self.model = model

    def get(self, slug):
        """
        Return a Post instance from the given slug.
        """
        markdown = _get_markdown_content(slug)
        return self.model(slug=slug, markdown=markdown)

    def all(self):
        """
        Return a list of all existing Post instances, in reverse alphabetical order.
        """
        pattern = '%s/*.md' % settings.TINYBLOG_ROOT_DIR
        filenames = glob(pattern)
        slugs = [os.path.relpath(f, settings.TINYBLOG_ROOT_DIR)[:-3] for f in filenames]  # [:-3] chops off the .md at the end
        return [self.model(slug=slug) for slug in sorted(slugs, reverse=True)]

    def count(self):
        return len(self.all())

    def __get__(self, instance, owner):
        return type(self)(model=owner)


class Post(object):
    slug = None
    markdown = None
    objects = PostManager()

    # quack like a duck
    _default_manager = objects

    def __init__(self, slug, markdown=None):
        self.slug = slug
        self._markdown = markdown

    @property
    def markdown(self):
        if self._markdown is not None:
            return self._markdown
        self._markdown = _get_markdown_content(self.slug)
        return self._markdown

    @cached_property
    def html(self):
        return md.markdown(self.markdown)

    @cached_property
    def intro_html(self):
        return md.markdown(self.markdown.split('---')[0])
