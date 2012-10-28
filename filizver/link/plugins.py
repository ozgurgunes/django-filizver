# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryType
from .forms import LinkForm

class LinkEntryPlugin(EntryType):
    name = 'link'
    title = 'Link'
    form_class = LinkForm
    link = reverse('filizver:link_create')
