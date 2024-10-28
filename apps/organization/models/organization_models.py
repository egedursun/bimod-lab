#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: organization_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    mission = models.TextField(null=True, blank=True)
    vision = models.TextField(null=True, blank=True)
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
    balance = models.DecimalField(max_digits=10, decimal_places=6, default=0.000000)
    organization_image_save_path = 'organization_images/%Y/%m/%d/'
    organization_image = models.ImageField(upload_to=organization_image_save_path, blank=True, max_length=1000,
                                           null=True)
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
