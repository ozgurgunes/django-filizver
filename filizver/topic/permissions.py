from permission import registry
from filizver.core.permissions import FilizverPermissionHandler
from models import Topic

class TopicPermissionHandler(FilizverPermissionHandler):

    def has_perm(self, user_obj, perm, obj=None):
        return super(TopicPermissionHandler, self).has_perm(user_obj, perm, obj)
        if user_obj.is_authenticated():
            if perm == 'filizver.add_topic':
                return True
            elif obj and obj.user == user_obj:
                return True
        # User doesn't have permission of ``perm``
        return False

registry.register(Topic, TopicPermissionHandler)