#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-11-24 20:06:56
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 20:06:56
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

from apps.voidforger.models import VoidForger
from config import settings

logger = logging.getLogger(__name__)


def generate_voidforger_endpoint(voidforger: VoidForger):
    logger.info(f"Generating VoidForger endpoint for assistant {voidforger.id}")
    organization_id = voidforger.llm_model.organization.id
    organization_name = voidforger.llm_model.organization.name
    llm_model_name = voidforger.llm_model.model_name
    creation_date = voidforger.created_at
    creation_year = creation_date.year
    creation_month = creation_date.month
    creation_day = creation_date.day
    randomness_constraint = "".join([str(random.choice(string.digits)) for _ in range(16)])
    return (f"{organization_id}/{''.join(ch for ch in organization_name if ch.isalnum())}/"
            f"{''.join(ch for ch in llm_model_name if ch.isalnum())}/{creation_year}/{creation_month}/{creation_day}"
            f"/{randomness_constraint}")


def generate_voidforger_custom_api_key(voidforger: VoidForger):
    logger.info(f"Generating custom API key for VoidForger {voidforger.id}")
    organization_id = voidforger.llm_model.organization.id
    organization_name = voidforger.llm_model.organization.name
    instructions = voidforger.llm_model.instructions
    llm_model_name = voidforger.llm_model.model_name
    llm_model_temperature = voidforger.llm_model.temperature
    llm_model_max_tokens = voidforger.llm_model.maximum_tokens
    llm_temperature = voidforger.llm_model.temperature
    salt = settings.ENCRYPTION_SALT
    randomness_constraint = [random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase)
                             for _ in range(64)]

    # merge the strings
    merged_string = (f"{instructions}{llm_model_name}"
                     f"{llm_model_temperature}{llm_model_max_tokens}{llm_temperature}{salt}{randomness_constraint}")
    # encrypt the merged string with SHA-256
    encrypted_string = ("Bearer bimod/" +
                        f"{str(organization_id)}/" +
                        f"{''.join(ch for ch in organization_name if ch.isalnum())}/" +
                        f"{''.join(ch for ch in llm_model_name if ch.isalnum())}/" +
                        hashlib.sha256(merged_string.encode()).hexdigest())
    return str(encrypted_string)
