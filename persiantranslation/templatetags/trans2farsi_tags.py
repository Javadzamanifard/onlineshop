from django import template

register = template.Library()


@register.filter
def en2fa(value):
    value = str(value)
    en2fa_trans = value.maketrans('0123456789', '۰١٢٣٤٥٦٧٨٩')
    return value.translate(en2fa_trans)