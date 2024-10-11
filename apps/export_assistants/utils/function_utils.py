#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import hashlib
import random
import string

from apps.assistants.models import Assistant
from config import settings


def generate_endpoint(assistant: Assistant):
    agent_id = assistant.id
    org_id = assistant.organization.id
    org_name = assistant.organization.name
    agent_name = assistant.name
    llm_name = assistant.llm_model.model_name
    date_created = assistant.created_at
    year_created = date_created.year
    month_created = date_created.month
    day_created = date_created.day
    randomness_constraint = "".join([str(random.choice(string.digits)) for _ in range(16)])
    return (f"{org_id}/{''.join(ch for ch in org_name if ch.isalnum())}/"
            f"{agent_id}/{''.join(ch for ch in agent_name if ch.isalnum())}/"
            f"{''.join(ch for ch in llm_name if ch.isalnum())}/{year_created}/{month_created}/{day_created}"
            f"/{randomness_constraint}")


def generate_assistant_custom_api_key(assistant: Assistant):
    agent_id = assistant.id
    org_id = assistant.organization.id
    org_name = assistant.organization.name
    agent_name = assistant.name
    desc = assistant.description
    instructions = assistant.instructions
    llm_name = assistant.llm_model.model_name
    llm_temperature = assistant.llm_model.temperature
    llm_max_tokens = assistant.llm_model.maximum_tokens
    salt = settings.ENCRYPTION_SALT
    randomness_constraint = [random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                             for _ in range(64)]
    merged_string = (f"{agent_id}{agent_name}{desc}{instructions}{llm_name}"
                     f"{llm_temperature}{llm_max_tokens}{llm_temperature}{salt}{randomness_constraint}")
    encrypted_string = ("Bearer bimod/" +
                        f"{str(org_id)}/" +
                        f"{''.join(ch for ch in org_name if ch.isalnum())}/" +
                        f"{str(agent_id)}/" +
                        f"{''.join(ch for ch in agent_name if ch.isalnum())}/" +
                        f"{''.join(ch for ch in llm_name if ch.isalnum())}/" +
                        hashlib.sha256(merged_string.encode()).hexdigest())
    return str(encrypted_string)
