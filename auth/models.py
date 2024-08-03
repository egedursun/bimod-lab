from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.user_permissions.models import UserPermission, PERMISSION_TYPES
from auth.utils import generate_random_string, generate_referral_code

REFERRAL_DEFAULT_BONUS_PERCENTAGE = 50


class UserCreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_cards')
    name_on_card = models.CharField(max_length=255, null=False, blank=False)
    card_number = models.CharField(max_length=16, null=False, blank=False)
    card_expiration_month = models.CharField(max_length=2, null=False, blank=False)
    card_expiration_year = models.CharField(max_length=2, null=False, blank=False)
    card_cvc = models.CharField(max_length=4, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name_on_card}"

    class Meta:
        verbose_name = "Credit Card"
        verbose_name_plural = "Credit Cards"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['user', 'name_on_card', 'card_number', 'created_at']),
            models.Index(
                fields=['user', 'name_on_card', 'card_number', 'card_expiration_month', 'card_expiration_year',
                        'card_cvc', 'created_at'])
        ]

    # convert every name_on_card letters to uppercase on save
    def save(self, *args, **kwargs):
        self.name_on_card = self.name_on_card.upper()
        super(UserCreditCard, self).save(*args, **kwargs)
        # add the card to the relevant user's credit cards
        self.user.profile.credit_cards.add(self)


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
    birthdate = models.DateField(default=timezone.now)
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)

    profile_picture_save_path = 'profile_pictures/%Y/%m/%d/' + generate_random_string()
    profile_picture = models.ImageField(upload_to=profile_picture_save_path, max_length=1000, blank=True,
                                        default='/profile_pictures/default.png')
    is_active = models.BooleanField(default=True)

    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile_created_by_users",
                                        default=1, blank=True, null=True)

    # Add permissions for users
    permissions = models.ManyToManyField(UserPermission, related_name='user_permissions', blank=True)
    # Credit card information for the subscription.
    credit_cards = models.ManyToManyField(UserCreditCard, related_name='user_credit_cards', blank=True)
    # user referral code
    referral_code = models.ForeignKey('PromoCode', on_delete=models.SET_NULL, related_name='referral_code', blank=True,
                                      null=True)
    sub_users = models.ManyToManyField(User, related_name='sub_users', blank=True)

    def __str__(self):
        return self.user.username

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.referral_code is None:
            promo_code = PromoCode.objects.create(
                user=self.user, code=generate_referral_code(),
                bonus_percentage_referrer=REFERRAL_DEFAULT_BONUS_PERCENTAGE,
                bonus_percentage_referee=REFERRAL_DEFAULT_BONUS_PERCENTAGE, is_active=True, current_referrals=0,
                max_referral_limit=5, datetime_limit=timezone.now() + timezone.timedelta(days=360)
            )
            self.referral_code = promo_code
        super(Profile, self).save(force_insert, force_update, using, update_fields)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, email=instance.email)
        if instance.is_superuser:
            for permission in PERMISSION_TYPES:
                UserPermission.objects.get_or_create(user=instance, permission_type=permission[0])
            permissions_of_user = UserPermission.objects.filter(user=instance)
            instance.profile.permissions.add(*permissions_of_user)
        # if no profile image assign the default in the media folder
        if not instance.profile.profile_picture:
            instance.profile.profile_picture = 'profile_pictures/default.png'
            instance.profile.save()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['email']),
            models.Index(fields=['user', 'email']),
            models.Index(fields=['user', 'email', 'is_verified']),
            models.Index(fields=['user', 'email', 'is_verified', 'created_at']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['first_name', 'last_name', 'created_at']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['phone_number', 'created_at']),
            models.Index(fields=['address']),
            models.Index(fields=['address', 'created_at']),
            models.Index(fields=['city']),
            models.Index(fields=['city', 'created_at']),
            models.Index(fields=['country']),
            models.Index(fields=['country', 'created_at']),
            models.Index(fields=['postal_code']),
            models.Index(fields=['postal_code', 'created_at']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_active', 'created_at']),
            models.Index(fields=['created_by_user']),
            models.Index(fields=['created_by_user', 'created_at']),
        ]


class PromoCode(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="promo_codes")
    code = models.CharField(max_length=255)
    bonus_percentage_referrer = models.IntegerField(default=REFERRAL_DEFAULT_BONUS_PERCENTAGE)
    bonus_percentage_referee = models.IntegerField(default=REFERRAL_DEFAULT_BONUS_PERCENTAGE)
    is_active = models.BooleanField(default=True)

    current_referrals = models.IntegerField(default=0)
    max_referral_limit = models.IntegerField(default=0)

    datetime_limit = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Promo Code"
        verbose_name_plural = "Promo Codes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]
