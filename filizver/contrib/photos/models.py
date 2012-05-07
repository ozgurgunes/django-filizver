import re
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from filizver.models import PostBase
from sorl.thumbnail import ImageField, delete
from filizver import signals

def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), str(instance._meta.module_name), re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))

class Photo(PostBase):
    """Photo model"""

    DISPLAY_CHOICES = (
        ('L', _('Left')),
        ('N', _('None')),
        ('R', _('Right')),
    )
    image           = models.ImageField(upload_to=get_upload_to, width_field='image_width', height_field='image_height', blank=False, null=False)
    title           = models.CharField(max_length=128, blank=True, null=True)
    description     = models.TextField(blank=True, null=True)

    display         = models.CharField(choices=DISPLAY_CHOICES, default='N', max_length=1, blank=True, null=True)

    image_width     = models.IntegerField(editable=False, null=True)
    image_height    = models.IntegerField(editable=False, null=True)

    class Meta:
        verbose_name            = _('Photo')
        verbose_name_plural     = _('Photos')

    def __unicode__(self):
        return u"%s" % self.image

    def delete(self):
        delete(self.image)
        super(Photo, self).delete()

    @models.permalink
    def get_absolute_url(self):
        return ('photos_photo_detail', None, {'id': self.id })

    @models.permalink
    def get_update_url(self):
        return ('photos_photo_update', None, {'id': self.id })

    @models.permalink
    def get_delete_url(self):
        return ('photos_photo_delete', None, {'id': self.id })

post_save.connect(signals.add_post_signal, sender=Photo)
post_delete.connect(signals.delete_post_signal, sender=Photo)