# -*- coding: utf-8 -*-
from filizver.entry.plugins import EntryType
from filizver.branch.forms import BranchForm


class BranchEntry(EntryType):
    name = 'branch'
    title = 'Branch'
    form_class = BranchForm

