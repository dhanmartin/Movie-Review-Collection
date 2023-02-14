from django import template


register = template.Library()


@register.filter
def active_menu(active, menu):
    if active == menu:
        return "active"
    else:
        return ""
