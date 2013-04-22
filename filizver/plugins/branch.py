# -*- coding: utf-8 -*-
from filizver.plugins.entry import EntryPoint
from filizver.forms.branch import BranchForm


class BranchEntry(EntryPoint):
    name = 'branch'
    title = 'Branch'
    form_class = BranchForm
    link = reverse('filizver:branch_create')
