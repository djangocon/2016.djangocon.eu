from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


_ACTION_TPL = '''
    <li>
        <a href="{url}" title="{title}">
            <span class="glyphicon glyphicon-{icon}" aria-hidden="true"></span>
        </a>
    </li>
'''

@register.simple_tag()
def toolbox(instance, user):
    """
    Render the toolbox list for the given model instance (with the given user).
    """
    actions = instance.get_toolbox(user)
    rendered_actions = '\n'.join(format_html(_ACTION_TPL, **action._asdict()) for action in actions)
    return mark_safe('<ul class="toolbox">{}</ul>'.format(rendered_actions))
