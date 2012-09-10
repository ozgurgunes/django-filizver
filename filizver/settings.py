# -*- coding: utf-8 -*-
# Filizver settings file.
#
# Please consult the docs for more information about each setting.

from django.conf import settings
gettext = lambda s: s


VARIABLE = getattr(settings,
                                'FILIZVER_VARIABLE',
                                None)
