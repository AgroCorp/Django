from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def readable_measure(value, group):
    print(value, group)
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


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None