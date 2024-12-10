#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-22 02:44:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 02:44:36
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
import uuid

import wonderwords

logger = logging.getLogger(__name__)


def generate_random_chart_file_name():
    uuid_field_1 = str(uuid.uuid4())
    uuid_field_2 = str(uuid.uuid4())

    merged_name = uuid_field_1 + uuid_field_2

    return merged_name


def generate_random_elite_agent_name():
    logger.info("Generating chat name.")

    name_adjective_component = wonderwords.RandomWord().word(
        word_max_length=8,
        include_categories=["adjective"]
    )

    name_noun_component = wonderwords.RandomWord().word(
        word_max_length=8,
        include_categories=["noun"]
    )

    name_adjective_capitalized = name_adjective_component.capitalize()

    name_noun_capitalized = name_noun_component.capitalize()

    return " ".join(
        [
            name_adjective_capitalized,
            name_noun_capitalized
        ]
    )
