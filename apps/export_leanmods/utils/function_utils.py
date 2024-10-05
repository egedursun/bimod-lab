#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

import hashlib
import random
import string

from apps.leanmod.models import LeanAssistant
from config import settings


def generate_leanmod_assistant_endpoint(assistant: LeanAssistant):
    assistant_id = assistant.id
    organization_id = assistant.organization.id
    organization_name = assistant.organization.name
    assistant_name = assistant.name
    llm_model_name = assistant.llm_model.model_name

    creation_date = assistant.created_at
    creation_year = creation_date.year
    creation_month = creation_date.month
    creation_day = creation_date.day
    randomness_constraint = "".join([str(random.choice(string.digits)) for _ in range(16)])
    return (f"{organization_id}/{''.join(ch for ch in organization_name if ch.isalnum())}/"
            f"{assistant_id}/{''.join(ch for ch in assistant_name if ch.isalnum())}/"
            f"{''.join(ch for ch in llm_model_name if ch.isalnum())}/{creation_year}/{creation_month}/{creation_day}"
            f"/{randomness_constraint}")


def generate_leanmod_assistant_custom_api_key(assistant: LeanAssistant):
    assistant_id = assistant.id
    organization_id = assistant.organization.id
    organization_name = assistant.organization.name
    assistant_name = assistant.name
    instructions = assistant.instructions
    llm_model_name = assistant.llm_model.model_name
    llm_model_temperature = assistant.llm_model.temperature
    llm_model_max_tokens = assistant.llm_model.maximum_tokens
    llm_temperature = assistant.llm_model.temperature
    salt = settings.ENCRYPTION_SALT
    randomness_constraint = [random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                             for _ in range(64)]

    # merge the strings
    merged_string = (f"{assistant_id}{assistant_name}{instructions}{llm_model_name}"
                     f"{llm_model_temperature}{llm_model_max_tokens}{llm_temperature}{salt}{randomness_constraint}")
    # encrypt the merged string with SHA-256
    encrypted_string = ("Bearer bimod/" +
                        f"{str(organization_id)}/" +
                        f"{''.join(ch for ch in organization_name if ch.isalnum())}/" +
                        f"{str(assistant_id)}/" +
                        f"{''.join(ch for ch in assistant_name if ch.isalnum())}/" +
                        f"{''.join(ch for ch in llm_model_name if ch.isalnum())}/" +
                        hashlib.sha256(merged_string.encode()).hexdigest())
    return str(encrypted_string)
