from permission import registry, PermissionHandler
from models import Board

class BoardPermissionHandler(PermissionHandler):

    def has_perm(self, user_obj, perm, obj=None):
        """
        board.add_board
        board.view_board
        board.change_board
        board.delete_board
        board.moderate_board
        board.add_entry
        board.change_entry
        board.delete_entry
        board.add_comment
        
        """
        if user_obj.is_authenticated():
            if user_obj.is_superuser or user_obj.is_staff:
                return True
            elif perm == 'filizver.add_topic':
                return True
            elif obj and obj.user == user_obj:
                return True
            elif obj and perm == 'board.change_board' \
                        and user_obj in obj.topic.moderators:
                return True
            elif obj and perm == 'board.moderate_board' \
                        and user_obj in obj.topic.moderators:
                return True
            elif obj and perm == 'board.moderate_board' \
                        and user_obj in obj.topic.moderators:
                return True
            elif obj and perm == 'board.add_entry' \
                        and user_obj in obj.topic.followers:
                return True
        # User doesn't have permission of ``perm``
        return False

registry.register(Board, BoardPermissionHandler)