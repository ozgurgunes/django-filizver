# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from filizver.models import Topic

site = Site.objects.get_current()

from django.utils.translation import ugettext_lazy as _

class TopicLatestRSS(Feed):

    title_template = 'filizver/feed_title.html'
    description_template = 'filizver/feed_description.html'
        
    title = _('%s Latest') % site.name
    link = "/"
    description = _('Updates on %s') % site.name

    def items(self):
        return Topic.objects.order_by('-date_created')[:10]
        
    def item_pubdate(self,item):
        #For each item, what is the pubdate?
        return item.date_created

    def item_author_name(self, item):
        return item.user


class TopicLatestAtom(TopicLatestRSS):

    feed_type   = Atom1Feed
    subtitle    = TopicLatestRSS.description
    
