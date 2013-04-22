# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filizver.models.entry import AbstractEntry
from filizver.utils import defaults, text


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

    
class Text(AbstractEntry):

    html            = models.TextField(_('HTML'), blank=True, null=True)
    markup          = models.CharField(_('Markup'), max_length=15, 
                            choices=MARKUP_CHOICES, default=defaults.DEFAULT_MARKUP)

    class Meta:
        verbose_name            = _('text')
        verbose_name_plural     = _('texts')

    def __unicode__(self):
        return u"%s" % self.body[:64] + '...' if len(self.body) > 64 else ''

    def save(self, *args, **kwargs):
        self.html = utils.text_to_html(self.body, self.markup)
        if defaults.SMILEYS_SUPPORT: #and self.user.profile.smileys:
            self.html = utils.smileys(self.html)
        super(Text, self).save(*args, **kwargs)
