from django import template

register = template.Library()


@register.filter
def chunkify(seq, size):
    """
    Break up a given list in sub-lists of the given size.
    """
    for i in range(0, len(seq), size):
        yield seq[i:i+size]
