# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from filizver.entry.plugins import EntryType
from forms import BranchForm


class BranchEntry(EntryType):
    name = 'branch'
    title = 'Branch'
    form_class = BranchForm
    link = reverse('filizver:branch_create')

    def create(self, request):
        super(BranchEntry, self).create(request)
