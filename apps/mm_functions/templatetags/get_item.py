
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_function_ids(dictionary, key):
    item = dictionary.get(key)
    ids = []
    for i in item:
        ids.append(i.custom_function.id)
    return ids
