"""
Module Overview: This module defines the `Organization` model within an assistant-based application. The model represents an organization entity, storing its details, associated users, assistants, and related configurations such as balance and image. It also includes relationships with other models like `LLMCore`, `ExportAssistantAPI`, and `AutoBalanceTopUpModel`.

Dependencies:
- `django.db.models`: Django's ORM for defining database models.
- `apps.organization.utils.generate_random_string`: Utility function to generate random strings for file paths.
"""

from django.db import models


class Organization(models.Model):
    """
    Organization Model:
    - Purpose: Represents an organization within the system, storing key details such as name, contact information, industry, and status. It also manages relationships with users, assistants, language models, and other configurations like auto balance top-ups.
    - Key Fields:
        - `name`: The name of the organization.
        - `email`: Contact email for the organization.
        - `phone`: Contact phone number for the organization.
        - `address`: Physical address of the organization.
        - `city`, `country`, `postal_code`: Fields for storing the organization's location details.
        - `industry`: The industry in which the organization operates.
        - `is_active`: Boolean field indicating whether the organization is active.
        - `created_at`, `updated_at`: Timestamps for creation and last update.
        - `created_by_user`: ForeignKey linking to the `User` who created the organization.
        - `last_updated_by_user`: ForeignKey linking to the `User` who last updated the organization.
        - `balance`: Decimal field representing the organization's current balance.
        - `organization_image`: ImageField for storing the organization's profile image, with a dynamically generated save path.
        - `users`: ManyToManyField linking to the `User` model, representing the users associated with the organization.
        - `llm_cores`: ManyToManyField linking to the `LLMCore` model, representing the language models associated with the organization.
        - `exported_assistants`: ManyToManyField linking to the `ExportAssistantAPI` model, representing the exported assistants associated with the organization.
        - `auto_balance_topup`: OneToOneField linking to the `AutoBalanceTopUpModel` for managing automatic balance top-ups.
    - Meta:
        - `verbose_name`: "Organization"
        - `verbose_name_plural`: "Organizations"
        - `ordering`: Orders organizations by creation date in descending order.
        - `indexes`: Indexes on various fields for optimized queries, including `name`, `email`, `phone`, `industry`, `is_active`, `balance`, and timestamps.
    """

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                        related_name="organization_created_by_users", blank=True, null=True)
    last_updated_by_user = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                                             related_name="organization_last_updated_by_users", blank=True, null=True)

    # additional fields
    balance = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)

    # profile image
    organization_image_save_path = 'organization_images/%Y/%m/%d/'
    organization_image = models.ImageField(upload_to=organization_image_save_path, blank=True, max_length=1000,
                                           null=True)
    # many to many fields
    users = models.ManyToManyField("auth.User", related_name="organizations")

    auto_balance_topup = models.OneToOneField("llm_transaction.AutoBalanceTopUpModel",
                                              on_delete=models.SET_NULL, blank=True, null=True,
                                              related_name="organization_auto_balance_topup")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["industry"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["last_updated_by_user"]),
            models.Index(fields=["balance"]),
        ]



