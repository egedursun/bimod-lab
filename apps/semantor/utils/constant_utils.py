#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-09 15:05:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 15:05:26
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

from config.settings import BASE_DIR


class OpenAIEmbeddingModels:
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_ADA_V2 = "text-embedding-ada-002"


VECTOR_INDEX_PATH_ASSISTANTS = os.path.join(BASE_DIR, 'vectors', 'semantor_vectors', 'assistants')
VECTOR_INDEX_PATH_LEANMOD_ASSISTANTS = os.path.join(BASE_DIR, 'vectors', 'semantor_vectors', 'leanmod_assistants')
VECTOR_INDEX_PATH_INTEGRATIONS = os.path.join(BASE_DIR, 'vectors', 'semantor_vectors', 'integrations')

ANNOY_DEFAULT_NUMBER_OF_TREES = 10

ASSISTANT_VECTOR_DATA_ADMIN_LIST = ('created_at', 'updated_at')
ASSISTANT_VECTOR_DATA_ADMIN_FILTER = ('created_at', 'updated_at')
ASSISTANT_VECTOR_DATA_ADMIN_SEARCH = ('assistant__name', 'assistant__organization__name')

LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_LIST = ('created_at', 'updated_at')
LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_FILTER = ('created_at', 'updated_at')
LEANMOD_ASSISTANT_VECTOR_DATA_ADMIN_SEARCH = ('leanmod_assistant__name', 'assistant__organization__name')

INTEGRATION_VECTOR_DATA_ADMIN_LIST = ['id', 'created_at', 'updated_at']
INTEGRATION_VECTOR_DATA_ADMIN_SEARCH = ['id']
INTEGRATION_VECTOR_DATA_ADMIN_FILTER = ['created_at', 'updated_at']

OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS = 3072

SEMANTOR_CONFIGURATION_ADMIN_LIST = ['user', 'is_local_network_active', 'is_global_network_active',
                                     'maximum_assistant_search_items', 'maximum_integration_search_items',
                                     'created_at', 'updated_at']
SEMANTOR_CONFIGURATION_ADMIN_FILTER = ['is_local_network_active', 'is_global_network_active',
                                       'maximum_assistant_search_items', 'maximum_integration_search_items',
                                       'created_at', 'updated_at']
SEMANTOR_CONFIGURATION_ADMIN_SEARCH = ['user__username']
