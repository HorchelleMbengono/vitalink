from django import template
register = template.Library()

@register.filter
def dict_get(dictionnaire, cle):
    return dictionnaire.get(cle)
