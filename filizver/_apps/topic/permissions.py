from permission import registry, PermissionHandler
from models import Topic

class TopicPermissionHandler(PermissionHandler):

    def has_perm(self, user, perm, obj=None):
        """
        topic.add_topic
        topic.view_topic
        topic.change_topic
        topic.delete_topic
        topic.moderate_topic
        topic.add_entry
        topic.change_entry
        topic.delete_entry
        topic.add_comment
        
        """
        if user.is_authenticated():
            if user.is_superuser:
                return True
            elif obj and obj.user == user:
                return True
            elif perm == 'filizver.add_topic':
                return True
            elif obj and perm in (
                            'topic.change_topic', 
                            'topic.moderate_topic', 
                            'topic.add_entry'
                        ) and user in obj.topic.moderators:
                return True
        # User doesn't have permission of ``perm``
        return False

registry.register(Topic, TopicPermissionHandler)
