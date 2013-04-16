# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from timezones.fields import TimeZoneField

#from manifest.profiles.models import ProfileBase
from filizver.topic.models import Topic
from filizver.core.utils import get_upload_to
from filizver.core.fields import AutoOneToOneField

from manifest.accounts.managers import ProfileBaseManager

class ProfileManager(ProfileBaseManager):
    pass

class Profile(models.Model):

    GENDER_CHOICES = (
        ('F', _(u'Female')),
        ('M', _(u'Male')),
    )
    
    user = models.OneToOneField(User, unique=True, verbose_name=_(u'User'), 
                related_name='profile')
    
    topic = AutoOneToOneField(Topic, parent_link=True, related_name='profile')

    birth_date = models.DateField(_(u'Birth date'), blank=True, null=True)

    gender = models.CharField(_(u'Gender'), choices=GENDER_CHOICES, 
                max_length=1, blank=True, null=True)

    picture = models.ImageField(_(u'Picture'), blank=True, 
                upload_to=get_upload_to)

    timezone = TimeZoneField(_(u"Timezone"))

    locale = models.CharField(_(u"Locale"), max_length = 10,
                                    choices = settings.LANGUAGES,
                                    default = settings.LANGUAGE_CODE)
                                    
    objects = ProfileManager()

    class Meta:
        app_label           = 'filizver'
        verbose_name        = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering            = ('topic__title',)
        
    def __unicode__(self):
        return self.topic.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('filizver:profile_detail', None, {'username': self.user.username })
        
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        try:
            old_obj = self.__class__.objects.get(pk=self.pk)
            if old_obj.picture.path != self.picture.path:
                path = old_obj.picture.path
                default_storage.delete(path)
        except:
            pass
        super(Profile, self).save(force_insert, force_update, 
                                        *args, **kwargs)

    @property
    def avatar(self):
        return self.get_picture_url()
        
    # Forum attrs
    def markup(self):
        pass
    def auto_subscribe(self):
        pass

    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.birth_date:
            return u"%s" % relativedelta.relativedelta(TODAY, 
                                self.birth_date).years
        else:
            return None
