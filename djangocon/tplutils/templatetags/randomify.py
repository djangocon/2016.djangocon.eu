import contextlib
import random

from django import template
from django.template.defaultfilters import date as dateformat
from django.utils import timezone

register = template.Library()


@contextlib.contextmanager
def seedrandom(seed=None, *args, **kwargs):
    previous_state = random.getstate()
    if seed is not None:
        random.seed(seed, *args, **kwargs)
    yield
    random.setstate(previous_state)


@register.filter
def randomify(seq, seed=None):
    """
    Shuffle the given sequence using a seed if provided
    """
    seq = list(seq)
    if seed is None:
        random.shuffle(seq)
        return seq
    with seedrandom(seed):
        random.shuffle(seq)
        return seq


@register.filter
def randomify_by_date(seq, format_string='Ymd'):
    """
    Shuffle the givens sequence but uses a seed based on the current date and
    time. You can pass a format string to control how often the randomization
    will change.

    For example:
    
        Ymd (the default) will change every day
        Ymdhi will change every minute
        Y will change every year
        ...
    """
    seed = dateformat(timezone.now(), format_string)
    return randomify(seq, seed)
