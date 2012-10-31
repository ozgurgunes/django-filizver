from permission import registry, PermissionHandler
from models import Project

class ProjectPermissionHandler(PermissionHandler):

    def has_perm(self, user_obj, perm, obj=None):
        """
        project.add_project
        project.view_project
        project.change_project
        project.delete_project
        project.moderate_project
        project.add_entry
        project.change_entry
        project.delete_entry
        project.add_comment
        
        """
        if user_obj.is_authenticated():
            if user_obj.is_superuser or user_obj.is_staff:
                return True
            elif perm == 'filizver.add_topic':
                return True
            elif obj and obj.user == user_obj:
                return True
            elif obj and perm == 'project.change_project' \
                        and user_obj in obj.topic.moderators:
                return True
            elif obj and perm == 'project.moderate_project' \
                        and user_obj in obj.topic.moderators:
                return True
            elif obj and perm == 'project.moderate_project' \
                        and user_obj in obj.topic.moderators:
                return True
            elif obj and perm == 'project.add_entry' \
                        and user_obj in obj.topic.followers:
                return True
        # User doesn't have permission of ``perm``
        return False

registry.register(Project, ProjectPermissionHandler)