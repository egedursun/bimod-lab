from django.db import models

from apps.user_permissions.utils import PERMISSION_TYPES


class ActiveUserPermissionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class UserPermission(models.Model):
    """
    UserPermission Model:
    - Purpose: Represents the permissions assigned to users within the application. Each permission is linked to a specific user and can be toggled as active or inactive.
    - Key Fields:
        - `user`: ForeignKey linking to the `User` who has been assigned the permission.
        - `permission_type`: The specific type of permission assigned, chosen from a predefined set of permission types.
        - `is_active`: Boolean field indicating whether the permission is currently active.
        - `created_at`: Timestamp for when the permission was created.
    - Methods:
        - `get_permission_type_name()`: Returns the human-readable name of the permission type.
        - `get_permission_type_code()`: Returns the code for the permission type.
    - Managers:
        - `active_permissions`: Custom manager for retrieving only active permissions.
    - Meta:
        - `verbose_name`: "User Permission"
        - `verbose_name_plural`: "User Permissions"
        - `ordering`: Orders permissions by the creation date in descending order.
        - `constraints`: Ensures that each user can have only one unique permission type.
        - `indexes`: Indexes on various fields for optimized queries, including combinations of `user`, `permission_type`, `is_active`, and `created_at`.
    """

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="permissions", null=True)
    permission_type = models.CharField(max_length=255, choices=PERMISSION_TYPES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()  # The default manager.
    active_permissions = ActiveUserPermissionManager()  # Custom manager for active permissions.

    class Meta:
        verbose_name = "User Permission"
        verbose_name_plural = "User Permissions"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=['user', 'permission_type'], name='unique_user_permission')
        ]
        indexes = [
            models.Index(fields=['user', 'permission_type']),
            models.Index(fields=['user', 'permission_type', 'is_active']),
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['permission_type', 'is_active']),
            models.Index(fields=['permission_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['permission_type', 'created_at']),
            models.Index(fields=['user', 'permission_type', 'created_at']),
            models.Index(fields=['user', 'permission_type', 'is_active', 'created_at']),
            models.Index(fields=['user', 'is_active', 'created_at']),
            models.Index(fields=['permission_type', 'is_active', 'created_at']),
        ]

    def get_permission_type_name(self):
        return dict(PERMISSION_TYPES)[self.permission_type]

    def get_permission_type_code(self):
        return self.permission_type
