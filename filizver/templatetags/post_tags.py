from django.contrib.contenttypes.models import ContentType
from django import template
from django.conf import settings
from django.template.loader import select_template

from filizver.models import Entry

register = template.Library()

def render_item(item, template_name=None):
    model_name = item.content_object._meta.verbose_name_raw

    template_list = [template_name,] if template_name else []
    template_list.extend([
        'tumblelog/_entry_%(model)s.html' % {'model': model_name },
        'tumblelog/_entry_default.html'
    ])

    t = select_template(template_list)

    return t.render(template.Context({
        'object' : item.content_object,
        'object_id' : item.id,
        'content_type' : item.content_type,
        'item': item,
        'MEDIA_URL': settings.MEDIA_URL
    }))

register.filter('render_item', render_item)
