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
import os
import uuid

from django.core.files import File
from django.core.files.storage import default_storage
from django.db import models

from apps.ml_model_store.utils import (
    MODEL_CATEGORIES,
    MLModelIntegrationCategoriesNames
)
from config import settings


class MLModelIntegration(models.Model):
    model_category = models.CharField(
        max_length=255,
        choices=MODEL_CATEGORIES,
        default=MLModelIntegrationCategoriesNames.MISCELLANEOUS
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    model_image = models.ImageField(
        upload_to='integration_ml_model_images/%Y/%m/%d/',
        null=True,
        blank=True
    )

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

    def save(self, *args, **kwargs):
        super(MLModelIntegration, self).save(*args, **kwargs)

        if not self.model_image:

            static_image_directory = os.path.join(
                settings.STATIC_ROOT,
                'img',
                'ml_model_store'
            )

            if self.model_category == MLModelIntegrationCategoriesNames.COMPUTER_VISION:

                img_file_name = "computer-vision.png"

            elif self.model_category == MLModelIntegrationCategoriesNames.NATURAL_LANGUAGE_PROCESSING:

                img_file_name = "natural-language-processing.png"

            elif self.model_category == MLModelIntegrationCategoriesNames.GENERATIVE_AI:

                img_file_name = "generative-ai.png"

            elif self.model_category == MLModelIntegrationCategoriesNames.GRAPH_MACHINE_LEARNING:

                img_file_name = "graph-machine-learning.png"

            elif self.model_category == MLModelIntegrationCategoriesNames.MISCELLANEOUS:

                img_file_name = "miscellaneous.png"

            else:

                img_file_name = "miscellaneous.png"

            with open(
                os.path.join(
                    static_image_directory,
                    img_file_name
                ),
                "rb"
            ) as image_file:

                unique_filename = f'integration_ml_model_images/{uuid.uuid4()}.png'

                default_storage.save(
                    unique_filename,
                    File(image_file)
                )

                self.model_image.name = unique_filename

                self.save()
