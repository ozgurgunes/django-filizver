# -*- coding: utf-8 -*-
import re
from django.contrib.sites.models import Site
from django.utils.translation import force_unicode, check_for_language
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


def get_upload_to(instance, filename):
    return '%s/%s/%s' % (str(instance._meta.app_label), 
                            str(instance._meta.module_name), 
                            re.sub('[^\.0-9a-zA-Z()_-]', '_', filename))


def absolute_url(path):
    return 'http://%s%s' % (Site.objects.get_current().domain, path)
    

def set_language(request, language):
    """
    Change the language of session of authenticated user.
    """

    if check_for_language(language):
        request.session['django_language'] = language

def prefetch_related(weak_queryset):
    """
    http://djangosnippets.org/snippets/2492/
    
    """
    gfks = {}
    for name, gfk in weak_queryset.model.__dict__.items():
        if not isinstance(gfk, generic.GenericForeignKey):
            continue
        gfks[name] = gfk

    data = {}
    for weak_model in weak_queryset:
        for gfk_name, gfk_field in gfks.items():
            related_content_type_id = getattr(weak_model, gfk_field.model._meta.get_field_by_name(gfk_field.ct_field)[0].get_attname())
            if not related_content_type_id:
                continue
            related_content_type = ContentType.objects.get_for_id(related_content_type_id)
            related_object_id = int(getattr(weak_model, gfk_field.fk_field))

            if related_content_type not in data.keys():
                data[related_content_type] = []
            data[related_content_type].append(related_object_id)

    for content_type, object_ids in data.items():
        model_class = content_type.model_class()
        models = prefetch_related(model_class.objects.filter(pk__in=object_ids))
        for model in models:
            for weak_model in weak_queryset:
                for gfk_name, gfk_field in gfks.items():
                    related_content_type_id = getattr(weak_model, gfk_field.model._meta.get_field_by_name(gfk_field.ct_field)[0].get_attname())
                    if not related_content_type_id:
                        continue
                    related_content_type = ContentType.objects.get_for_id(related_content_type_id)
                    related_object_id = int(getattr(weak_model, gfk_field.fk_field))
                    
                    if related_object_id != model.pk:
                        continue
                    if related_content_type != content_type:
                        continue

                    setattr(weak_model, gfk_name, model)

    return weak_queryset