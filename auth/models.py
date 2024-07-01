from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from auth.utils import generate_random_string


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, unique=True)  # Use unique=True for unique email addresses
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

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, email=instance.email)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
