#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_002_llm_core_create.py
#  Last Modified: 2024-11-18 20:40:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:40:08
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

from apps.llm_core.models import LLMCore
from apps.llm_core.utils import GPTModelNamesNames
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__002_llm_core_create(
    metadata__user,
    metadata__organization,
    response__llm_core_openai_api_key,
    response__openai_temperature
):
    try:
        new_llm_model = LLMCore.objects.create(
            organization=metadata__organization,
            created_by_user=metadata__user,
            last_updated_by_user=metadata__user,
            provider="OA",
            api_key=response__llm_core_openai_api_key,
            temperature=response__openai_temperature,
            model_name=GPTModelNamesNames.GPT_4O,
            nickname="General Core Model" + " " + generate_random_object_id_string(),
            description="The primary LLM core model generated for organization " + metadata__organization.name + ".",
        )
    except Exception as e:
        logger.error(f"Error in action__002_llm_core_create: {e}")
        return False, None

    logger.info("action__002_llm_core_create completed successfully.")
    return True, new_llm_model
