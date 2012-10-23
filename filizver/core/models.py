# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class DateMixin(models.Model):
    created_date            = models.DateTimeField(_('Created date'), auto_now_add=True, 
                                        editable=False, blank=False, null=False)
    updated_date            = models.DateTimeField(_('Updated date'), auto_now=True, 
                                        editable=False, blank=True, null=True)
    updated_user            = models.ForeignKey(User, verbose_name=_('Updated user'), 
                                        related_name='updated_%(class)s_set', blank=True, null=True)
    
    class Meta:
        abstract = True

        
class DeleteMixin(models.Model):
    deleted                 = models.BooleanField(_('Deleted'), default=False)
    deleted_date            = models.DateTimeField(_('Deleted date'), 
                                        editable=False, blank=True, null=True)
    deleted_user            = models.ForeignKey(User, verbose_name=_('Deleted user'), 
                                        related_name='deleted_%(class)s_set', blank=True, null=True)
    
    class Meta:
        abstract = True
        
    def delete(self, *args, **kwargs):
        commit = kwargs.pop('commit', False)
        request = kwargs.pop('request', None)
        if commit:
            return super(DeleteMixin, self).delete(*args, **kwargs)
        if not self.deleted:
            self.deleted = True
            self.deleted_date = datetime.datetime.now()
            if request:
                self.deleted_user = request.user
            self.save()
        