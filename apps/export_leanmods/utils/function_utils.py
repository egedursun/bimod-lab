#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
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
import logging
import random
import string

from apps.leanmod.models import LeanAssistant
from config import settings


logger = logging.getLogger(__name__)


def generate_leanmod_assistant_endpoint(assistant: LeanAssistant, export_id: int):
    logger.info(f"Generating LeanMod Assistant Endpoint for Assistant: {assistant}")
    org_id = assistant.organization.id
    assistant_id = assistant.id
    export_id = export_id

    endpoint_str = f"{str(org_id)}/{str(assistant_id)}/{str(export_id)}/"
    return endpoint_str

def generate_leanmod_assistant_custom_api_key(assistant: LeanAssistant):
    logger.info(f"Generating LeanMod Assistant Custom API Key for Assistant: {assistant}")
    agent_id = assistant.id
    org_id = assistant.organization.id
    org_name = assistant.organization.name
    agent_name = assistant.name
    instructions = assistant.instructions
    llm_model_name = assistant.llm_model.model_name
    llm_model_temperature = assistant.llm_model.temperature
    llm_model_max_tokens = assistant.llm_model.maximum_tokens
    llm_temperature = assistant.llm_model.temperature
    salt = settings.ENCRYPTION_SALT
    randomness_constraint = [random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                             for _ in range(64)]
    merged_string = (f"{agent_id}{agent_name}{instructions}{llm_model_name}"
                     f"{llm_model_temperature}{llm_model_max_tokens}{llm_temperature}{salt}{randomness_constraint}")
    encrypted_string = ("Bearer bimod/" +
                        f"{str(org_id)}/" +
                        f"{''.join(ch for ch in org_name if ch.isalnum())}/" +
                        f"{str(agent_id)}/" +
                        f"{''.join(ch for ch in agent_name if ch.isalnum())}/" +
                        f"{''.join(ch for ch in llm_model_name if ch.isalnum())}/" +
                        hashlib.sha256(merged_string.encode()).hexdigest())
    return str(encrypted_string)
