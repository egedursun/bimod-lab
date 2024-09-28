from django.contrib.auth.models import User

from apps.user_permissions.models import UserPermission
from apps.user_permissions.utils import PermissionNames


class UserPermissionManager:
    @staticmethod
    def is_authorized(user: User, operation: str):
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list('permission_type', flat=True)
        if operation not in user_permissions:
            print(f"[UserPermissionManager.is_authorized]: User {user.username} is not authorized to "
                  f"perform operation {operation}.")
            return False
        return True
