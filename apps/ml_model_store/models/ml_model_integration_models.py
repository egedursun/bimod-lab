#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ml_model_integration_models.py
#  Last Modified: 2024-11-08 14:38:49
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-08 14:38:49
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

from apps.ml_model_store.utils import (
    MODEL_CATEGORIES,
    MLModelIntegrationCategoriesNames
)


class MLModelIntegration(models.Model):
    model_category = models.CharField(
        max_length=255,
        choices=MODEL_CATEGORIES,
        default=MLModelIntegrationCategoriesNames.MISCELLANEOUS
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    model_image_url = models.URLField(null=True, blank=True)
    model_download_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.model_category

    class Meta:
        verbose_name = "ML Model Integration"
        verbose_name_plural = "ML Model Integrations"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "model_category"
            ]),
            models.Index(fields=[
                "created_at"
            ]),
            models.Index(fields=[
                "updated_at"
            ])
        ]
