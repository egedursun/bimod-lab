#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integration_vector_data_admin.py
#  Last Modified: 2024-11-09 18:19:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 18:19:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


"""
#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: integration_vector_data_models.py
#  Last Modified: 2024-11-09 15:09:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 15:09:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import json
import os

import openai
from annoy import AnnoyIndex
from django.db import models

from apps.semantor.utils.constant_utils import OpenAIEmbeddingModels, VECTOR_INDEX_PATH_INTEGRATIONS, \
    ANNOY_DEFAULT_NUMBER_OF_TREES


class IntegrationVectorData(models.Model):
    integration_assistant = models.ForeignKey('integrations.AssistantIntegration', on_delete=models.CASCADE)

    raw_data = models.JSONField()
    vector_data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.integration_assistant.integration_name

    class Meta:
        verbose_name = 'Integration Vector Data'
        verbose_name_plural = 'Integration Vector Data'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        raw_data= {
            "assistant_name": self.integration_assistant.integration_name,
            "assistant_description": self.integration_assistant.integration_description,
            "assistant_instructions": self.integration_assistant.integration_instructions,
            "tools": {
                "image_generation_capability": False,
                "time_awareness": False,
                "place_awareness": False,
                "reasoning_capability_choice": "N/A",
            },
            "data_sources": {},
        }

        # Add tools
        raw_data['tools']['image_generation_capability'] = self.integration_assistant.integration_image_generation_capability
        raw_data['tools']['time_awareness'] = self.integration_assistant.integration_time_awareness
        raw_data['tools']['place_awareness'] = self.integration_assistant.integration_location_awareness
        raw_data['tools']['reasoning_capability_choice'] = self.integration_assistant.integration_multi_step_reasoning

        self.raw_data = raw_data

        ##############################
        # Convert to Vector
        ##############################

        # Convert raw_data to a JSON string for embedding generation
        raw_data_text = json.dumps(raw_data, indent=2)
        try:
            response = openai.Embedding.create(
                input=raw_data_text,
                model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE,
            )
            embedding_vector = response['data'][0]['embedding']
            self.vector_data = embedding_vector
        except Exception as e:
            print("Error generating embedding:", e)
            self.vector_data = []

        ##############################
        # Save the Index to Vector DB
        ##############################

        super().save(*args, **kwargs)

        if self.vector_data:
            vector_dim = len(self.vector_data)
            index_path = os.path.join(VECTOR_INDEX_PATH_INTEGRATIONS, 'annoy_index.ann')
            annoy_index = AnnoyIndex(vector_dim, 'angular')

            # Load existing index if it exists
            if os.path.exists(index_path):
                annoy_index.load(index_path)

            annoy_index.add_item(self.id, self.vector_data)
            annoy_index.build(ANNOY_DEFAULT_NUMBER_OF_TREES)
            annoy_index.save(index_path)

"""

from django.contrib import admin

from apps.semantor.models import IntegrationVectorData
from apps.semantor.utils.constant_utils import INTEGRATION_VECTOR_DATA_ADMIN_LIST, \
    INTEGRATION_VECTOR_DATA_ADMIN_SEARCH, INTEGRATION_VECTOR_DATA_ADMIN_FILTER


@admin.register(IntegrationVectorData)
class IntegrationVectorDataAdmin(admin.ModelAdmin):
    list_display = INTEGRATION_VECTOR_DATA_ADMIN_LIST
    search_fields = INTEGRATION_VECTOR_DATA_ADMIN_SEARCH
    list_filter = INTEGRATION_VECTOR_DATA_ADMIN_FILTER
    ordering = ['-created_at']
