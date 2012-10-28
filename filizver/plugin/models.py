from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import get_plugin_name, get_plugin_from_string


class PointManager(models.Manager):
    def get_point(self, point):
        return self.get(path=get_plugin_name(point))


class Point(models.Model):
    path    = models.CharField(_('Path'), max_length=255)
    title   = models.CharField(_('Title'), max_length=255)
    active  = models.BooleanField(_('Active'), default=True)

    objects = PointManager()

    class Meta:
        app_label   = 'filizver'
        db_table = 'filziver_plugin_point'

    def __unicode__(self):
        return self.title


class PluginManager(models.Manager):
    def get_plugin(self, plugin):
        return self.get(path=get_plugin_name(plugin))

    def get_plugins_of(self, point):
        return self.filter(point__path=get_plugin_name(point), active=True)

    def get_by_natural_key(self, name):
        return self.get(path=name)


class Plugin(models.Model):
    """
    Database representation of a plugin.

    Fields ``name`` and ``title`` are synchronized from plugin classes.

    point
        Plugin point.

    path
        Full python path to plugin class, including class too.

    name
        Plugin slug name, must be unique within one plugin point.

    title
        Eny verbose title of this plugin.

    position
        Using values from this field plugins are orderd.

    status
        Plugin status.
    """
    point       = models.ForeignKey(Point, verbose_name=_('Point'))
    path        = models.CharField(_('Path'), max_length=255, unique=True)
    name        = models.CharField(_('Name'), max_length=255, null=True, blank=True)
    title       = models.CharField(_('Title'), max_length=255, default='', blank=True)
    position    = models.IntegerField(_('Position'), default=0)
    active      = models.BooleanField(_('Active'), default=True)

    objects = PluginManager()

    class Meta:
        app_label   = 'filizver'
        unique_together = (("point", "name"),)
        order_with_respect_to = 'point'
        ordering = ('position', 'id')

    def __unicode__(self):
        if self.title:
            return self.title
        if self.name:
            return self.name
        return self.path

    def natural_key(self):
        return (self.path,)

    def is_active(self):
        return self.active

    def get_plugin(self):
        plugin_class = get_plugin_from_string(self.path)
        return plugin_class()
