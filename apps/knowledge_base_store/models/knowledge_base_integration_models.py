#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: knowledge_base_integration_models.py
#  Last Modified: 2024-12-21 19:09:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-21 19:09:31
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

from django.core.files.storage import (
    default_storage
)

from django.db import models

from apps.knowledge_base_store.utils import (
    KNOWLEDGE_BASE_CATEGORIES,
    KnowledgeBaseIntegrationCategoriesNames
)

from config import settings


class KnowledgeBaseIntegration(models.Model):
    knowledge_base_category = models.CharField(
        max_length=255,
        choices=KNOWLEDGE_BASE_CATEGORIES,
        default=KnowledgeBaseIntegrationCategoriesNames.MISCELLANEOUS,
    )

    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    knowledge_base_image = models.ImageField(
        upload_to='integration_knowledge_base_images/%Y/%m/%d/',
        null=True,
        blank=True
    )

    knowledge_base_download_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " - " + self.knowledge_base_category

    class Meta:
        verbose_name = "Knowledge Base Integration"
        verbose_name_plural = "Knowledge Base Integrations"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "knowledge_base_category"
            ]),
            models.Index(fields=[
                "created_at"
            ]),
            models.Index(fields=[
                "updated_at"
            ])
        ]

    def save(self, *args, **kwargs):
        super(KnowledgeBaseIntegration, self).save(*args, **kwargs)

        if not self.knowledge_base_image:

            static_image_directory = os.path.join(
                settings.STATIC_ROOT,
                'img',
                'knowledge_base_store'
            )

            if self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.SOFTWARE_AND_IT:

                img_file_name = "software-and-it.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.LEGAL_AND_LAW:

                img_file_name = "legal-and-law.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.HEALTHCARE_AND_MEDICINE:

                img_file_name = "healthcare-and-medicine.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.FINANCE_AND_BUSINESS:

                img_file_name = "finance-and-business.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.EDUCATION_AND_TRAINING:

                img_file_name = "education-and-training.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.SCIENCE_AND_ENGINEERING:

                img_file_name = "science-and-engineering.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.HISTORY_AND_CULTURE:

                img_file_name = "history-and-culture.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.SPORTS_AND_ENTERTAINMENT:

                img_file_name = "sports-and-entertainment.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.MILITARY_AND_DEFENSE:

                img_file_name = "military-and-defense.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.TRANSPORT_AND_LOGISTICS:

                img_file_name = "transport-and-logistics.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.AGRICULTURE_AND_FOOD:

                img_file_name = "agriculture-and-food.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.MEDIA_AND_COMMUNICATION:

                img_file_name = "media-and-communication.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.SPACE_AND_ASTRONOMY:

                img_file_name = "space-and-astronomy.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.ETHICS_AND_PHILOSOPHY:

                img_file_name = "ethics-and-philosophy.png"

            elif self.knowledge_base_category == KnowledgeBaseIntegrationCategoriesNames.MISCELLANEOUS:

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

                unique_filename = f'integration_knowledge_base_images/{uuid.uuid4()}.png'

                default_storage.save(
                    unique_filename,
                    File(image_file)
                )

                self.knowledge_base_image.name = unique_filename

                self.save()
