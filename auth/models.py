
from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from apps.user_permissions.models import UserPermission, PERMISSION_TYPES
from auth.utils import generate_random_string


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, unique=True)
    email_token = models.CharField(max_length=100, blank=True, null=True)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # additional fields
    username = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=60, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)

    profile_picture_save_path = 'profile_pictures/%Y/%m/%d/' + generate_random_string()
    profile_picture = models.ImageField(upload_to=profile_picture_save_path, blank=True, max_length=1000,
                                        null=True)
    is_active = models.BooleanField(default=True)

    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_created_by_users",
                                        default=1, blank=True, null=False)

    # Add permissions for users
    permissions = models.ManyToManyField(UserPermission, related_name='user_permissions', blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, email=instance.email)
        if instance.is_superuser:
            for permission in PERMISSION_TYPES:
                UserPermission.objects.get_or_create(user=instance, permission_type=permission[0])
            permissions_of_user = UserPermission.objects.filter(user=instance)
            instance.profile.permissions.add(*permissions_of_user)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
