#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
#
#

import random
import string

from apps.assistants.utils import RANDOM_SUFFIX_MAXIMUM_VALUE, RANDOM_SUFFIX_MINIMUM_VALUE


def generate_random_string(length=16):
    return ''.join(
        random.choice(
            string.ascii_letters + string.digits
        ) for _ in range(
            length
        )
    )


def generate_random_name_suffix():
    return f"{str(
        random.randint(
            RANDOM_SUFFIX_MINIMUM_VALUE,
            RANDOM_SUFFIX_MAXIMUM_VALUE
        )
    )}"
