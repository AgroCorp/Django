from django import template
register = template.Library()


@register.filter(name='convert_linebreak')
def convert_linebreak_to_html(value):
    new_value = value.replace('\r', '')
    new_value = new_value.replace('\n', '<br>')
    return new_value


@register.filter(name='upscale_measure')
def readable_measure(value, group):
    if group == 1:
        if value >= 1000:
            return value / 1000
        elif 1000 > value >= 100:
            return value / 100
        else:
            return value

    elif group == 2:
        if value >= 1000:
            return value / 1000
        elif 1000 > value >= 100:
            return value / 100
        else:
            return value
    else:
        return value


@register.filter(name='upscale_measure_2')
def readable_measure2(value, pre_name):
    from ..models import PreIngredients
    pre = PreIngredients.objects.get(measure=pre_name).multiply
    return value / pre
