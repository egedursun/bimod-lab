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

import hashlib
import json
import logging
import os

import faiss
import numpy as np
from django.db import models

from apps.semantor.utils.constant_utils import (
    OpenAIEmbeddingModels,
    VECTOR_INDEX_PATH_INTEGRATIONS,
    OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
)

from config import settings
from data.path_consts import DataPaths

logger = logging.getLogger(__name__)


class IntegrationVectorData(models.Model):
    integration_assistant = models.ForeignKey(
        'integrations.AssistantIntegration',
        on_delete=models.CASCADE
    )

    raw_data = models.JSONField(blank=True, null=True)

    raw_data_hash = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    vector_data = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.integration_assistant.integration_name

    class Meta:
        verbose_name = 'Integration Vector Data'
        verbose_name_plural = 'Integration Vector Data'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        raw_data = {
            "assistant_name": self.integration_assistant.integration_name,
            "assistant_description": self.integration_assistant.integration_description,
            "assistant_instructions": self.integration_assistant.integration_instructions,
            "included_in_meta_integration_teams": [],
            "tools": {
                "image_generation_capability": False,
                "time_awareness": False,
                "place_awareness": False,
                "reasoning_capability_choice": "N/A",
            },
            "data_sources": {},
        }

        # Add included teams
        #   - Load the JSON data for teams

        teams_meta_integrations_data_path = (
            DataPaths.CategoriesAndTeamsMetaIntegrations.TEAMS_META_INTEGRATIONS
        )

        with open(teams_meta_integrations_data_path, "r") as teams_integrations_file:
            teams_integrations_data_json = json.load(teams_integrations_file)

            for team_data in teams_integrations_data_json:

                if self.integration_assistant.integration_name in team_data["integration_assistants"]:
                    raw_data["included_in_meta_integration_teams"].append(
                        team_data["meta_integration_name"]
                    )

        # Add tools

        raw_data['tools'][
            'image_generation_capability'
        ] = self.integration_assistant.integration_image_generation_capability

        raw_data['tools'][
            'time_awareness'
        ] = self.integration_assistant.integration_time_awareness

        raw_data['tools'][
            'place_awareness'
        ] = self.integration_assistant.integration_location_awareness

        raw_data['tools'][
            'reasoning_capability_choice'
        ] = self.integration_assistant.integration_multi_step_reasoning

        self.raw_data = raw_data

        ##############################
        # Save the Index to Vector DB
        ##############################

        super().save(*args, **kwargs)

        self.raw_data = raw_data

        if (
            self.has_raw_data_changed() or
            self.vector_data is None or
            self.vector_data == []
        ):

            self._generate_embedding(raw_data)
            self._save_embedding()

        else:
            logger.info("Raw data has not changed; skipping embedding generation.")
            pass

    def _get_index_path(self):
        return os.path.join(
            VECTOR_INDEX_PATH_INTEGRATIONS,
            f'integrations_index.index'
        )

    def _generate_embedding(self, raw_data):
        from apps.core.generative_ai.gpt_openai_manager import (
            OpenAIGPTClientManager
        )

        c = OpenAIGPTClientManager.get_naked_client_with_api_key(
            api_key=settings.INTERNAL_OPENAI_API_KEY
        )

        raw_data_text = json.dumps(
            raw_data,
            indent=2
        )

        try:
            response = c.embeddings.create(
                input=raw_data_text,
                model=OpenAIEmbeddingModels.TEXT_EMBEDDING_3_LARGE
            )

            embedding_vector = response.data[0].embedding

            self.vector_data = embedding_vector

        except Exception as e:
            logger.error(f"Error in generating embedding: {e}")

            self.vector_data = []

    def _save_embedding(self):
        if self.vector_data:
            x = np.array(
                [
                    self.vector_data
                ],
                dtype=np.float32
            ).reshape(
                1,
                OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
            )

            xids = np.array(
                [
                    self.id
                ],
                dtype=np.int64
            )

            index_path = self._get_index_path()

            if not os.path.exists(index_path):
                index = faiss.IndexIDMap(
                    faiss.IndexFlatL2(
                        OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS
                    )
                )

            else:
                index = faiss.read_index(index_path)

                if not isinstance(
                    index,
                    faiss.IndexIDMap
                ):
                    index = faiss.IndexIDMap(index)

                index.remove_ids(xids)

            index.add_with_ids(
                x,
                xids
            )

            faiss.write_index(
                index,
                index_path
            )

    def has_raw_data_changed(self):
        raw_data_str = json.dumps(
            self.raw_data,
            sort_keys=True
        )

        new_raw_data_hash = hashlib.sha256(
            raw_data_str.encode('utf-8')
        ).hexdigest()

        if self.raw_data_hash == new_raw_data_hash:
            return False

        self.raw_data_hash = new_raw_data_hash

        return True
