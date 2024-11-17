#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: knowledge_base_decoder.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from apps.core.codebase.utils import KNOWLEDGE_BASE_PROVIDERS
from apps.core.vector_operations.vector_document.vector_store_executor import WeaviateExecutor


logger = logging.getLogger(__name__)


class KnowledgeBaseSystemDecoder:
    @staticmethod
    def get(connection):
        if connection.provider == KNOWLEDGE_BASE_PROVIDERS["WEAVIATE"]["code"]:
            logger.info("Using Weaviate as the knowledge base system")
            return WeaviateExecutor(connection)
