#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: custom_api_models.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
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

from apps.mm_apis.utils import CUSTOM_API_AUTHENTICATION_TYPES


class CustomAPI(models.Model):
    is_public = models.BooleanField(default=False)
    categories = models.JSONField(default=list, blank=True)
    name = models.CharField(max_length=10000, unique=True)
    description = models.TextField()
    authentication_type = models.CharField(max_length=5000, default="None", choices=CUSTOM_API_AUTHENTICATION_TYPES)
    authentication_token = models.CharField(max_length=5000, default="", blank=True)
    base_url = models.CharField(max_length=5000, default="")
    endpoints = models.JSONField(default=dict, blank=True)
    api_picture = models.ImageField(upload_to="custom_apis/%YYYY/%mm/%dd/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.created_at.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = "Custom API"
        verbose_name_plural = "Custom APIs"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["created_by_user"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"]),
            models.Index(fields=["is_public"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["name", "is_public"]),
            models.Index(fields=["name", "is_featured"]),
        ]
