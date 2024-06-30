import datetime

import django
from django.db import models
from django.utils import timezone

SUBSCRIPTION_PLANS = [
    ("free", "free"),
    ("starter", "starter"),
    ("grower", "grower"),
    ("enterprise", "enterprise"),
]

SUBSCRIPTION_COSTS = {
    "free": 0,
    "starter": 1000,
    "grower": 5000,
    "enterprise": 10000,
}

SUBSCRIPTION_BALANCE_DISCOUNT_RATES = {
    "free": 0.0,
    "starter": 0.10,
    "grower": 0.15,
    "enterprise": 0.20,
}

SUBSCRIPTION_LIMITS = {
    "free" : {
        "max_number_of_llm_cores": 1,
        "max_number_of_users": 3,
        "max_number_of_assistants": 1,
        "max_number_of_chats": 10,
        "orchestrations": 0,
        "long_term_memory": False,
        "providers": 0,
        "file_systems": 0,
        "web_browsers": 1,
        "sql_databases": 1,
        "knowledge_bases": 1,
        "documents": 5,
        "image_storage": False,
        "video_storage": False,
        "audio_storage": False,
        "functions": 3,
        "api": 3,
        "scheduled_jobs": 1,
        "triggers": 0,
        "image_gen_and_analysis": False,
        "audio_gen_and_analysis": False,
        "integrations": 0,
        "meta_integrations": 0,
    },
    "starter" : {
        "max_number_of_llm_cores": 5,
        "max_number_of_users": 20,
        "max_number_of_assistants": 10,
        "max_number_of_chats": 100_000_000,
        "orchestrations": 1,
        "long_term_memory": True,
        "providers": 10,
        "file_systems": 1,
        "web_browsers": 3,
        "sql_databases": 3,
        "knowledge_bases": 3,
        "documents": 1000,
        "image_storage": True,
        "video_storage": True,
        "audio_storage": True,
        "functions": 30,
        "api": 15,
        "scheduled_jobs": 10,
        "triggers": 10,
        "image_gen_and_analysis": True,
        "audio_gen_and_analysis": True,
        "integrations": 3,
        "meta_integrations": 0,
    },
    "grower" : {
        "max_number_of_llm_cores": 30,
        "max_number_of_users": 100,
        "max_number_of_assistants": 30,
        "max_number_of_chats": 100_000_000,
        "orchestrations": 10,
        "long_term_memory": True,
        "providers": 30,
        "file_systems": 10,
        "web_browsers": 10,
        "sql_databases": 10,
        "knowledge_bases": 10,
        "documents": 10_000,
        "image_storage": True,
        "video_storage": True,
        "audio_storage": True,
        "functions": 250,
        "api": 100,
        "scheduled_jobs": 50,
        "triggers": 50,
        "image_gen_and_analysis": True,
        "audio_gen_and_analysis": True,
        "integrations": 10,
        "meta_integrations": 3,
    },
    "enterprise" : {
        "max_number_of_llm_cores": 100_000_000,
        "max_number_of_users": 100_000_000,
        "max_number_of_assistants": 100_000_000,
        "max_number_of_chats": 100_000_000,
        "orchestrations": 100_000_000,
        "long_term_memory": True,
        "providers": 100_000_000,
        "file_systems": 100_000_000,
        "web_browsers": 100_000_000,
        "sql_databases": 100_000_000,
        "knowledge_bases": 100_000_000,
        "documents": 100_000_000,
        "image_storage": True,
        "video_storage": True,
        "audio_storage": True,
        "functions": 100_000_000,
        "api": 100_000_000,
        "scheduled_jobs": 100_000_000,
        "triggers": 100_000_000,
        "image_gen_and_analysis": True,
        "audio_gen_and_analysis": True,
        "integrations": 100_000_000,
        "meta_integrations": 100_000_000,
    },
}


SUBSCRIPTION_STATUSES = [
    ("free_starter", "free_starter"),
    ("active", "active"),
    ("missed_payment", "missed_payment"),
    ("cancelled", "cancelled"),
    ("on_trial", "on_trial"),
]


# Create your models here.

class Subscription(models.Model):
    user = models.ForeignKey('auth.User',
                             on_delete=models.CASCADE,
                             related_name='subscriptions')
    organization = models.ForeignKey('organization.Organization',
                                     on_delete=models.CASCADE,
                                     related_name='subscriptions')

    # Credit card information for the subscription.
    name_on_card = models.CharField(max_length=255, blank=True)
    card_number = models.CharField(max_length=16, blank=True)
    card_expiration_month = models.CharField(max_length=2, blank=True)
    card_expiration_year = models.CharField(max_length=2, blank=True)
    card_cvc = models.CharField(max_length=4, blank=True)

    # Subscription plan selection.
    subscription_plan = models.CharField(max_length=100, choices=SUBSCRIPTION_PLANS, default="free")
    subscription_cost = models.FloatField(choices=SUBSCRIPTION_COSTS, default=0.0)
    subscription_balance_discount_rate = models.FloatField(choices=SUBSCRIPTION_BALANCE_DISCOUNT_RATES, default=0.0)

    # Granted permission limits (automatically set based on the subscription plan).
    max_number_of_llm_cores = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["max_number_of_llm_cores"])
    max_number_of_users = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["max_number_of_users"])
    max_number_of_assistants = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["max_number_of_assistants"])
    max_number_of_chats = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["max_number_of_chats"])
    max_orchestrations = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["orchestrations"])
    max_providers = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["providers"])
    max_file_systems = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["file_systems"])
    max_web_browsers = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["web_browsers"])
    max_sql_databases = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["sql_databases"])
    max_knowledge_bases = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["knowledge_bases"])
    max_documents = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["documents"])
    max_functions = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["functions"])
    max_api = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["api"])
    max_scheduled_jobs = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["scheduled_jobs"])
    max_triggers = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["triggers"])
    max_integrations = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["integrations"])
    max_meta_integrations = models.IntegerField(default=SUBSCRIPTION_LIMITS["free"]["meta_integrations"])
    allow_long_term_memory = models.BooleanField(default=SUBSCRIPTION_LIMITS["free"]["long_term_memory"])
    allow_image_storage = models.BooleanField(default=SUBSCRIPTION_LIMITS["free"]["image_storage"])
    allow_video_storage = models.BooleanField(default=SUBSCRIPTION_LIMITS["free"]["video_storage"])
    allow_audio_storage = models.BooleanField(default=SUBSCRIPTION_LIMITS["free"]["audio_storage"])
    allow_image_gen_and_analysis = models.BooleanField(default=SUBSCRIPTION_LIMITS["free"]["image_gen_and_analysis"])
    allow_audio_gen_and_analysis = models.BooleanField(default=SUBSCRIPTION_LIMITS["free"]["audio_gen_and_analysis"])

    # Get current day of the month as the renewal date. (automatically set based on the creation date of the instances)
    renewal_day_of_month = models.IntegerField(default=timezone.now().day)
    subscription_status = models.CharField(max_length=100, choices=SUBSCRIPTION_STATUSES, default="free_starter")
    next_renewal_date = models.DateTimeField(default=django.utils.timezone.now() + datetime.timedelta(days=30))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name="created_subscriptions", default=1)
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name="updated_subscriptions", default=1)

    def __str__(self):
        return f"{self.organization.name} - {self.subscription_plan} - {self.created_at}"

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["-created_at"]

    def get_subscription_cost(self):
        return SUBSCRIPTION_COSTS[self.subscription_plan]

    def get_subscription_balance_discount_rate(self):
        return SUBSCRIPTION_BALANCE_DISCOUNT_RATES[self.subscription_plan]


# TODO: there needs to be a Cron Job / Payment Gateway Task to handle the subscription works
#   1. Every month, retrieve the "subscription amount" from the credit card.
#  2. If the amount is not paid, then the subscription status should be switched to "missed_payment", and the tier
#       must be switched to "free".
#  3. If the amount is paid, then the "next payment date" should be updated to the next month. The status
#       must stay "active".
#  4. If the subscription is cancelled, then the status must be switched to "cancelled" and the tier
#       must be switched to "free".
#  5. If the subscription is on trial, then the status must be switched to "on_trial" and the tier
#       must be switched to "free". The end date of the trial must be set to 30 days from the start date.
#       The subscription type must be "starter".
