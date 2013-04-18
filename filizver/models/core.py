# -*- coding: utf-8 -*-
import datetime
from mongoengine import *
from django.utils.translation import ugettext_lazy as _

from user import User

class DateMixin(object):
    created_date            = DateTimeField()
    updated_date            = DateTimeField(default=datetime.datetime.now)
    updated_user            = ReferenceField(User)
                                        
    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = datetime.datetime.now()
        return super(DateMixin, self).save(*args, **kwargs)


class DeleteMixin(object):
    deleted                 = BooleanField(default=False)
    deleted_date            = DateTimeField()
    deleted_user            = ReferenceField(User)

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
        

class UserMixin(DateMixin, DeleteMixin):
    ip_address      = StringField(max_length=15)
    api_gateway     = StringField(max_length=32)

