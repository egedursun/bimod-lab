#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_ellma_transcription_prompt.py
#  Last Modified: 2024-10-30 23:17:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-30 23:17:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.ellma.prompts import get_ellma_transcription_prompt
from apps.ellma.models import EllmaScript


def build_ellma_transcription_system_prompt(script: EllmaScript):
    merged_prompt = f""
    merged_prompt += get_ellma_transcription_prompt(script=script)

    return merged_prompt
