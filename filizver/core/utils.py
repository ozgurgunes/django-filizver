# -*- coding: utf-8 -*-
import re
from django.contrib.sites.models import Site

def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), 
                            str(instance._meta.module_name), 
                            re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))

def absolute_url(path):
    return 'http://%s%s' % (Site.objects.get_current().domain, path)