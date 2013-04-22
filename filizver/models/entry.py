# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth import get_user_model

from filizver.models.topic import Topic


class AbstractEntry(Topic):

    topic = models.OneToOneField(Topic, parent_link=True)

    class Meta:
        abstract        = True
        app_label       = 'filizver'
        ordering        = ('-created_date',)
        get_latest_by   = 'created_date'

    @models.permalink
    def get_absolute_url(self):
        return ('filizver_%s_detail' % self._meta.module_name.lower, None, {'id': self.id })

    def get_update_url(self):
        return ('filizver_%s_update' % self._meta.module_name.lower, None, {'id': self.id })

    def get_delete_url(self):
        return ('filizver_%s_delete' % self._meta.module_name.lower, None, {'id': self.id })

    def entry_template(self, template=None):
        if template == 'list':
            return u"%s/%s_entry_list.html" % (self._meta.app_label.lower(), self._meta.module_name.lower())
        elif template == 'detail':
            return u"%s/%s_entry_detail.html" % (self._meta.app_label.lower(), self._meta.module_name.lower())
        else:    
            return u"%s/%s_entry.html" % (self._meta.app_label.lower(), self._meta.module_name.lower())

