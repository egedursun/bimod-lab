from django import template


register = template.Library()


@register.filter
def convert_file_size(byte_size):
    kilobytes = byte_size / 1024
    stringified_kilobytes = f'{kilobytes:.2f} KB'
    return stringified_kilobytes
