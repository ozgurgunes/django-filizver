from permission import registry, PermissionHandler
from models import Project

class ProjectPermissionHandler(PermissionHandler):

    def has_perm(self, user_obj, perm, obj=None):
        return super(ProjectPermissionHandler, self).has_perm(user_obj, perm, obj)
        if user_obj.is_authenticated():
            if perm == 'filizver.add_topic':
                return True
            elif obj and obj.user == user_obj:
                return True
        # User doesn't have permission of ``perm``
        return False

registry.register(Topic, TopicPermissionHandler)