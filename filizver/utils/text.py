# -*- coding: utf-8 -*-
import re
from HTMLParser import HTMLParser, HTMLParseError
import defaults 

from django.template.defaultfilters import urlize as django_urlize

try:
    import markdown
except ImportError:
    pass
try:
    import textile
except ImportError:
    pass
try:
    import bbcode
except ImportError:
    pass


#compile smileys regex
_SMILEYS = [(re.compile(smiley_re), path) for smiley_re, path in defaults.SMILEYS]

class ExcludeTagsHTMLParser(HTMLParser):
    """
    Class for html parsing with excluding specified tags.
    """

    def __init__(self, func, tags=('a', 'pre', 'span')):
        HTMLParser.__init__(self)
        self.func = func
        self.is_ignored = False
        self.tags = tags
        self.html = []

    def handle_starttag(self, tag, attrs):
        self.html.append('<%s%s>' % (tag, self.__html_attrs(attrs)))
        if tag in self.tags:
            self.is_ignored = True

    def handle_data(self, data):
        if not self.is_ignored:
            data = self.func(data)
        self.html.append(data)

    def handle_startendtag(self, tag, attrs):
        self.html.append('<%s%s/>' % (tag, self.__html_attrs(attrs)))

    def handle_endtag(self, tag):
        self.is_ignored = False
        self.html.append('</%s>' % (tag))

    def handle_entityref(self, name):
        self.html.append('&%s;' % name)

    def handle_charref(self, name):
        self.html.append('&#%s;' % name)

    def unescape(self, s):
        #we don't need unescape data (without this possible XSS-attack)
        return s

    def __html_attrs(self, attrs):
        _attrs = ''
        if attrs:
            _attrs = ' %s' % (' '.join([('%s="%s"' % (k, v)) for k, v in attrs]))
        return _attrs

    def feed(self, data):
        HTMLParser.feed(self, data)
        self.html = ''.join(self.html)
        
def urlize(html):
    """
    Urlize plain text links in the HTML contents.
   
    Do not urlize content of A and CODE tags.
    """
    try:
        parser = ExcludeTagsHTMLParser(django_urlize)
        parser.feed(html)
        urlized_html = parser.html
        parser.close()
    except HTMLParseError:
        # HTMLParser from Python <2.7.3 is not robust
        # see: http://support.djangobb.org/topic/349/
        if settings.DEBUG:
            raise
        return html
    return urlized_html

def _smiley_replacer(data):
    for smiley, path in _SMILEYS:
        data = smiley.sub(path, data)
    return data

def smileys(html):
    """
    Replace text smileys.
    """
    try:
        parser = ExcludeTagsHTMLParser(_smiley_replacer)
        parser.feed(html)
        smileyd_html = parser.html
        parser.close()
    except HTMLParseError:
        # HTMLParser from Python <2.7.3 is not robust
        # see: http://support.djangobb.org/topic/349/
        if settings.DEBUG:
            raise
        return html
    return smileyd_html


def text_to_html(text, markup):
    if markup == 'bbcode':
        text = bbcode.render_html(text)
    elif markup == 'markdown':
        text = markdown.markdown(text, safe_mode='escape')
    elif markup == 'textile':
        text = textile.textile(text, safe_mode='escape')
    else:
        raise Exception('Invalid markup property: %s' % markup)
    return urlize(text)    
