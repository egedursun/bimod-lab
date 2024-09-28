from django import template

from config import settings

register = template.Library()


@register.simple_tag
def default_application_zoom():
    return str(str(settings.DEFAULT_APPLICATION_ZOOM) + "%")
