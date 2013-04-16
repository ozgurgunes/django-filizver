# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryPoint
from .forms import LinkForm

class LinkEntryPlugin(EntryPoint):
    name = 'link'
    title = 'Link'
    form_class = LinkForm
    link = reverse('filizver:link_create')
