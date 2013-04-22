# -*- coding: utf-8 -*-
from filizver.plugins.entry import EntryPoint
from filizver.forms.link import LinkForm


class LinkEntry(EntryPoint):
    name = 'link'
    title = 'Link'
    form_class = LinkForm
    link = reverse('filizver:link_create')
