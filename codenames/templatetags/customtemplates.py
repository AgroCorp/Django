from django import template
register = template.Library()


@register.inclusion_tag('codenames/wordCard.html', name='word_card')
def render_gamecard(word, class_name):
    return {'word': word, 'class': class_name}
