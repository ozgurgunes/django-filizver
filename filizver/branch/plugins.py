# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryPoint
from forms import BranchForm


class BranchEntry(EntryPoint):
    name = 'branch'
    title = 'Branch'
    form_class = BranchForm
    link = reverse('filizver:branch_create')

    def create(self, request):
        return super(BranchEntry, self).create(request)
