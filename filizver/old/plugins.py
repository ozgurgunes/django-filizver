# -*- coding: utf-8 -*-
from filizver.models import EntryType
from filizver.forms import BranchForm


class BranchEntry(EntryType):
    name = 'branch'
    title = 'Branch'
    form_class = BranchForm

