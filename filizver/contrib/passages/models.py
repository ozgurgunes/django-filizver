from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete
from filizver.models import PostBase
from filizver import signals

class Passage(PostBase):
    """Passage model"""

    body            = models.TextField(blank=False, null=False)
    footnote        = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name            = _('Passage')
        verbose_name_plural     = _('Passages')

    def __unicode__(self):
        return u"%s" % self.body
        
    @models.permalink
    def get_absolute_url(self):
        return ('passages_passage_detail', None, {'id': self.id })

    @models.permalink
    def get_update_url(self):
        return ('passages_passage_update', None, {'id': self.id })

    @models.permalink
    def get_delete_url(self):
        return ('passages_passage_delete', None, {'id': self.id })

post_save.connect(signals.add_post_signal, sender=Passage)
post_delete.connect(signals.delete_post_signal, sender=Passage)