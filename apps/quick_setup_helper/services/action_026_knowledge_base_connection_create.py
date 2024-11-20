#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_026_knowledge_base_connection_create.py
#  Last Modified: 2024-11-18 22:27:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:27:36
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

from apps.assistants.models import Assistant
from apps.datasource_knowledge_base.models import DocumentKnowledgeBaseConnection
from apps.llm_core.models import LLMCore
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__026_knowledge_base_connection_create(
    metadata__organization,
    metadata__llm_core,
    metadata__assistants,
    response__internal_data_sources__knowledge_base_provider,
    response__internal_data_sources__knowledge_base_host_url,
    response__internal_data_sources__knowledge_base_provider_api_key
):
    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            try:
                metadata__llm_core: LLMCore
                DocumentKnowledgeBaseConnection.objects.create(
                    assistant=assistant,
                    name=f"Primary Document Knowledge Base for assistant {assistant.name} {generate_random_object_id_string()}",
                    description=f"This is the primary Document Knowledge Base connection for the assistant {assistant.name} and organization {metadata__organization.name}.",
                    provider=response__internal_data_sources__knowledge_base_provider,
                    host_url=response__internal_data_sources__knowledge_base_host_url,
                    provider_api_key=response__internal_data_sources__knowledge_base_provider_api_key,
                    vectorizer="text2vec-openai",
                    vectorizer_api_key=metadata__llm_core.api_key
                )

            except Exception as e:
                logger.error(f"Failed to create Document Knowledge Base connection for assistant {assistant.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__026_knowledge_base_connection_create: {str(e)}")
        return False

    logger.info("action__026_knowledge_base_connection_create completed successfully.")
    return True
