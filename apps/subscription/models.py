"""

import datetime

import django
from django.db import models
from django.utils import timezone


SUBSCRIPTION_PLANS = [
    ("free", "free"),
    ("starter", "starter"),
    ("professional", "professional"),
    ("unlimited", "unlimited"),
    ############
]

SUBSCRIPTION_COSTS_MONTHLY = {
    "free": 0,
    "starter": 990.99,
    "professional": 1990.99,
    "unlimited": 4990.99,
}

SUBSCRIPTION_COSTS_ANNUALLY = {
    "free": 0,
    "starter": 990.99 * 12 * 0.9,
    "professional": 1990.99 * 12 * 0.8,
    "unlimited": 4990.99 * 12 * 0.6,
}

RENEWAL_MODES = [
    ("monthly", "monthly"),
    ("annual", "annual"),
]


SUBSCRIPTION_MESSAGE_LIMITS = {
    "free": 100,
    "starter": int(1000),
    "professional": int(10_000),
    "unlimited": int(100_000_000_000),
}


# Create your models here.

class Subscription(models.Model):
    user = models.ForeignKey('auth.User',
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    credit_card = models.ForeignKey('auth.UserCreditCard', on_delete=models.CASCADE, related_name='subscriptions',
                                    blank=True, null=True)

    # Subscription plan selection.
    subscription_plan = models.CharField(max_length=100, choices=SUBSCRIPTION_PLANS, default="free")

    # Get current day of the month as the renewal date. (automatically set based on the creation date of the instances)
    subscription_start_date = models.DateField(default=django.utils.timezone.now)
    subscription_end_date = models.DateField(default=django.utils.timezone.now)
    auto_renew = models.BooleanField(default=True)
    auto_renew_mode = models.CharField(max_length=100, choices=RENEWAL_MODES, default="monthly")

    ################################################################
    # Subscription limits
    ################################################################
    subscription_message_limit = models.IntegerField(default=SUBSCRIPTION_MESSAGE_LIMITS["free"])
    ################################################################

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_plan} - {self.created_at}"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-created_at"]

"""
