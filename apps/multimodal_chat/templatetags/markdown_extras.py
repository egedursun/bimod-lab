import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdownify')
def markdownify(text):
    return mark_safe(markdown.markdown(text))
