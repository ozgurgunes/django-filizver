from django.template import Library, Node, Variable, TemplateSyntaxError

from filizver.entry.models import Entry
from filizver.core.utils import prefetch_related

register = Library()


class EntriesNode(Node):
    def __init__(self, object, var_name):
        self.object = Variable(object)
        self.var_name = var_name

    def render(self, context):
        qs = Entry.objects.filter(topic_id=self.object.resolve(context)).select_related('user__profile')
        entries = prefetch_related(qs)
        context[self.var_name] = entries
        return ''


@register.tag
def get_entries(parser, token):
    contents = token.split_contents()
    if len(contents) != 4:
        raise TemplateSyntaxError("%r tag requires exactly 3 arguments" %
                                  (contents[0]))
    if 'as' != contents[2]:
        raise TemplateSyntaxError("%r tag 2nd argument must be 'as'" %
                                  (contents[0]))
    return EntriesNode(contents[1], contents[3])