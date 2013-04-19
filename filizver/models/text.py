# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from filizver.entry.models import EntryBase, add_entry_signal, delete_entry_signal
import defaults, utils

MARKUP_CHOICES = []
try:
    import markdown
    MARKUP_CHOICES.append(("markdown", "Markdown"))
except ImportError:
    pass
try:
    import textile
    MARKUP_CHOICES.append(("textile", "Textile"))
except ImportError:
    pass
try:
    import postmarkup
    MARKUP_CHOICES.append(('bbcode', 'BBCode'))
except ImportError:
    pass


    
class Text(EntryBase):
    """Passage model"""

    body            = models.TextField(_('Body'), blank=False, null=False)
    html            = models.TextField(_('HTML'), blank=True, null=True)
    markup          = models.CharField(_('Markup'), max_length=15, default=defaults.DEFAULT_MARKUP, choices=MARKUP_CHOICES)

    class Meta:
        app_label                = 'filizver'
        verbose_name            = _('Text')
        verbose_name_plural     = _('Texts')

    def __unicode__(self):
        return u"%s" % self.body[:64] + '...' if len(self.body) > 64 else ''

    def save(self, *args, **kwargs):
        self.html = utils.text_to_html(self.body, self.markup)
        if defaults.SMILEYS_SUPPORT: #and self.user.profile.smileys:
            self.html = utils.smileys(self.html)
        super(Text, self).save(*args, **kwargs)
        

post_save.connect(add_entry_signal, sender=Text)
post_delete.connect(delete_entry_signal, sender=Text)        
