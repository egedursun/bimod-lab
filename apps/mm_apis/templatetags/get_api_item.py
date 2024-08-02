from django import template

register = template.Library()


@register.filter
def get_api_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_api_ids(dictionary, key):
    item = dictionary.get(key)
    ids = []
    for i in item:
        ids.append(i.custom_api.id)
    return ids
