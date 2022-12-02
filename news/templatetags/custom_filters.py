from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    profanity = ['банан', 'апельсин']
    for word in profanity:
        if word in value:
            value = value.replace(word, '**')
    return value
