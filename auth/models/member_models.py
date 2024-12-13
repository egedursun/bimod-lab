#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: member_models.py
#  Last Modified: 2024-10-09 19:21:14
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:21:15
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import secrets

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.metatempo.utils import (
    META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH
)

from apps.user_permissions.models import (
    UserPermission
)

from apps.user_permissions.utils import (
    PERMISSION_TYPES
)

from auth.utils import (
    USER_FORUM_ROLES,
    USER_FORUM_RANKS,
    POINT_REWARDS,
    UNIT_REWARD_FOR_POINTS,
    RANK_POINT_REQUIREMENTS,
    generate_referral_code,
    REFERRAL_DEFAULT_BONUS_PERCENTAGE
)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        blank=True,
        null=True
    )

    email = models.EmailField(max_length=100, unique=True)

    email_token = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    forget_password_token = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    username = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=250,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=60,
        blank=True,
        null=True
    )

    birthdate = models.DateField(default=timezone.now)

    if birthdate is None or birthdate == '':
        birthdate = timezone.now()

    address = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    postal_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    free_credits = models.FloatField(default=0)

    is_accredited_by_staff = models.BooleanField(default=False)
    accreditation_email_sent_at = models.DateTimeField(null=True, blank=True)

    user_forum_role = models.CharField(
        max_length=100,
        choices=USER_FORUM_ROLES,
        default='client_user'
    )

    user_forum_rank = models.CharField(
        max_length=100,
        choices=USER_FORUM_RANKS,
        default='unranked'
    )

    user_forum_points = models.IntegerField(default=0)

    user_highest_ever_forum_points = models.IntegerField(default=0)
    user_last_forum_post_at = models.DateTimeField(null=True, blank=True)
    user_last_forum_comment_at = models.DateTimeField(null=True, blank=True)

    profile_picture_save_path = 'profile_pictures/%Y/%m/%d/'

    profile_picture = models.ImageField(
        upload_to=profile_picture_save_path,
        max_length=1000,
        blank=True,
        default='/profile_pictures/default.png'
    )

    is_active = models.BooleanField(default=True)

    created_by_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profile_created_by_users",
        blank=True, null=True
    )

    referral_code = models.ForeignKey(
        'PromoCode',
        on_delete=models.SET_NULL,
        related_name='referral_code',
        blank=True,
        null=True
    )

    sub_users = models.ManyToManyField(
        User,
        related_name='sub_users',
        blank=True
    )

    automated_data_backups = models.BooleanField(default=False)

    notifications = models.ManyToManyField(
        'notifications.NotificationItem',
        related_name='notifications',
        default=list,
        blank=True
    )

    metatempo_tracking_auth_key = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def add_points(self, action):
        points = POINT_REWARDS.get(action, 0)

        old_points = self.user_forum_points
        old_highest_points = self.user_highest_ever_forum_points

        self.user_forum_points += points

        if self.user_forum_points > self.user_highest_ever_forum_points:
            self.user_highest_ever_forum_points = self.user_forum_points

        self.save()

        try:
            if (old_points + points) > old_highest_points:
                user_rank_category = self.user_forum_rank

                user_rank_prize = UNIT_REWARD_FOR_POINTS.get(
                    user_rank_category,
                    0
                )

                total_prize = (points * user_rank_prize)

                self.free_credits += total_prize
                self.save()

        except Exception as e:
            pass

        self.save()
        self.update_rank()

    def remove_points(self, action):
        points = POINT_REWARDS.get(
            action,
            0
        )

        self.user_forum_points -= points

        self.save()
        self.update_rank()

    def update_rank(self):
        for rank, points in RANK_POINT_REQUIREMENTS.items():

            if self.user_forum_points >= points:
                self.user_forum_rank = rank
                self.save()

            else:
                break
        pass

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(
        sender,
        instance,
        created,
        **kwargs
    ):
        from auth.models import (
            PromoCode
        )

        if created:
            Profile.objects.create(
                user=instance,
                email=instance.email
            )

        if instance.is_superuser:
            for permission in PERMISSION_TYPES:
                UserPermission.objects.get_or_create(
                    user=instance,
                    permission_type=permission[0]
                )

            permissions_of_user = UserPermission.objects.filter(
                user=instance
            )

            instance.permissions.add(*permissions_of_user)

        if not instance.profile.profile_picture:
            instance.profile.profile_picture = 'profile_pictures/default.png'

            instance.profile.save()

        if instance.profile.referral_code is None:
            promo_code = PromoCode.objects.create(
                user=instance,
                code=generate_referral_code(),
                bonus_percentage_referrer=REFERRAL_DEFAULT_BONUS_PERCENTAGE,
                bonus_percentage_referee=REFERRAL_DEFAULT_BONUS_PERCENTAGE,
                is_active=True,
                current_referrals=0,
                max_referral_limit=5,
                datetime_limit=timezone.now() + timezone.timedelta(days=360)
            )

            instance.profile.referral_code = promo_code

            instance.profile.save()

        else:
            pass

        if instance.profile.metatempo_tracking_auth_key is None:
            instance.profile.metatempo_tracking_auth_key = secrets.token_urlsafe(
                META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH
            )

            instance.profile.save()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                'user'
            ]),
            models.Index(fields=[
                'email'
            ]),
            models.Index(fields=[
                'user',
                'email'
            ]),
            models.Index(fields=[
                'user',
                'email',
                'is_verified'
            ]),
            models.Index(fields=[
                'user',
                'email',
                'is_verified',
                'created_at'
            ]),
            models.Index(fields=[
                'first_name',
                'last_name'
            ]),
            models.Index(fields=[
                'first_name',
                'last_name',
                'created_at'
            ]),
            models.Index(fields=[
                'phone_number'
            ]),
            models.Index(fields=[
                'phone_number',
                'created_at'
            ]),
            models.Index(fields=[
                'address'
            ]),
            models.Index(fields=[
                'address',
                'created_at'
            ]),
            models.Index(fields=[
                'city'
            ]),
            models.Index(fields=[
                'city',
                'created_at'
            ]),
            models.Index(fields=[
                'country'
            ]),
            models.Index(fields=[
                'country',
                'created_at'
            ]),
            models.Index(fields=[
                'postal_code'
            ]),
            models.Index(fields=[
                'postal_code',
                'created_at'
            ]),
            models.Index(fields=[
                'is_active'
            ]),
            models.Index(fields=[
                'is_active',
                'created_at'
            ]),
            models.Index(fields=[
                'created_by_user'
            ]),
            models.Index(fields=[
                'created_by_user',
                'created_at'
            ]),
        ]
