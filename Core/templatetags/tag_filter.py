from django import template

register = template.Library()


@register.filter
def tag_filter(value):
    return value.replace(" ", "-")


@register.filter
def list_cast(list, cast):
    return list.filter(cast__title=cast)[:4]


@register.filter
def list_limit(list, count):
    return list[:count]


@register.filter
def check_category_checkbox(value, category):
    if value.find(category) != -1:
        return 'checked'
    return ''
