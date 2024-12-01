#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-09 17:10:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-09 17:10:57
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


OPEN_AI_DEFAULT_EMBEDDING_VECTOR_DIMENSIONS = 3072

VECTOR_INDEX_PATH_ASSISTANTS = os.path.join(BASE_DIR, 'semantor_vectors', 'assistants')
VECTOR_INDEX_PATH_LEANMOD_ASSISTANTS = os.path.join(BASE_DIR, 'semantor_vectors', 'leanmod_assistants')
VECTOR_INDEX_PATH_INTEGRATIONS = os.path.join(BASE_DIR, 'semantor_vectors', 'integrations')

SEMANTOR_DEFAULT_SEARCH_RESULTS_ASSISTANTS = 5
SEMANTOR_DEFAULT_SEARCH_RESULTS_LEANMOD_ASSISTANTS = 5
SEMANTOR_DEFAULT_SEARCH_RESULTS_INTEGRATIONS = 5
