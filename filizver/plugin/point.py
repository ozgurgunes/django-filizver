from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from .models import Plugin, Point as PointModel
from .utils import get_plugin_name

_PLUGIN_POINT = "<class 'filizver.plugin.point.PluginPoint'>"


def is_plugin_point(cls):
    return repr(cls.__base__) == _PLUGIN_POINT


class PluginMount(type):
    """
    See: http://martyalchin.com/2008/jan/10/simple-plugin-framework/

    """

    points = []

    def __new__(meta, class_name, bases, class_dict):
        cls = type.__new__(meta, class_name, bases, class_dict)
        if is_plugin_point(cls):
            PluginMount.points.append(cls)
        return cls

    def __init__(cls, name, bases, attrs):
        if is_plugin_point(cls):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        elif hasattr(cls, 'plugins'):
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

    DoesNotExist = ObjectDoesNotExist


class PluginPoint(object):
    __metaclass__ = PluginMount

    @classmethod
    def get_path(cls):
        return get_plugin_name(cls)

    @classmethod
    def is_active(cls):
        if is_plugin_point(cls):
            raise Exception(_('This method is only available to plugin '
                              'classes.'))
        else:
            return cls.get_model().is_active()


    @classmethod
    def get_model(cls, name=None, active=True):
        """
        Returns model instance of plugin point or plugin, depending from which
        class this methos is called.

        Example::

            plugin_model_instance = MyPlugin.get_model()
            plugin_model_instance = MyPluginPoint.get_model('plugin-name')
            plugin_point_model_instance = MyPluginPoint.get_model()

        """
        path = cls.get_pythonpath()
        if is_plugin_point(cls):
            if name is not None:
                kwargs = {}
                if status is not None:
                    kwargs['active'] = active
                return Plugin.objects.get(point__path=ppath,
                                          name=name, **kwargs)
            else:
                return PluginPointModel.objects.get(path=path)
        else:
            return Plugin.objects.get(path=ppath)

    @classmethod
    def get_point(cls):
        """
        Returns plugin point model instance. Only used from plugin classes.
        """
        if is_plugin_point(cls):
            raise Exception(_('This method is only available to plugin '
                              'classes.'))
        else:
            return cls.__base__

    @classmethod
    def get_point_model(cls):
        """
        Returns plugin point model instance. Only used from plugin classes.
        """
        if is_plugin_point(cls):
            raise Exception(_('This method is only available to plugin '
                              'classes.'))
        else:
            return PluginPointModel.objects.\
                    get(plugin__path=cls.get_path())

    @classmethod
    def get_plugins(cls):
        """
        Returns all plugin instances of plugin point, passing all args and
        kwargs to plugin constructor.
        """
        if is_plugin_point(cls):
            for plugin_model in cls.get_plugins_qs():
                yield plugin_model.get_plugin()
        else:
            raise Exception(_('This method is only available to plugin point '
                              'classes.'))

    @classmethod
    def get_plugins_qs(cls):
        """
        Returns query set of all plugins belonging to plugin point.

        Example::

            for plugin_instance in MyPluginPoint.get_plugins_qs():
                print(plugin_instance.get_plugin().name)

        """
        if is_plugin_point(cls):
            point_path = cls.get_path()
            return Plugin.objects.filter(point__path=point_path,
                                         active=True).order_by('position')
        else:
            raise Exception(_('This method is only available to plugin point '
                              'classes.'))

    @classmethod
    def get_name(cls):
        if is_plugin_point(cls):
            raise Exception(_('This method is only available to plugin '
                              'classes.'))
        else:
            return cls.get_model().name

    @classmethod
    def get_title(cls):
        if is_plugin_point(cls):
            raise Exception(_('This method is only available to plugin '
                              'classes.'))
        else:
            return cls.get_model().title
