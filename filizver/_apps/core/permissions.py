from permission import registry
from permission import PermissionHandler

from models import YourModel

class FilizverPermissionHandler(PermissionHandler):
    """Permission handler class for ``YourModel``. Similar with AdminSite"""
    def has_perm(self, user_obj, perm, obj=None):
        """this is called for checking permission of the model."""
        if user_obj.is_authenticated():
            if perm == 'yourapp.add_yourmodel':
                # Authenticated user has add permissions of this model
                return True
            elif obj and obj.author == user_obj:
                # Otherwise (change/delete) user must be an author
                return True
        # User doesn't have permission of ``perm``
        return False

# register this ``YourModelPermissionHandler`` with ``YourModel``
#registry.register(YourModel, YourModelPermissionHandler)