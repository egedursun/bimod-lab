#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_voidforger_communication_language_prompt.py
#  Last Modified: 2024-11-16 00:50:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 00:50:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.assistants.utils import AGENT_SPEECH_LANGUAGES


def build_communication_language_prompt_voidforger(response_language):
    return f"""
        ### **RESPONSE LANGUAGE:**

        '''
        {response_language}
        '''

        **NOTE**: This is the language that you will be using while providing responses. If this part is named
        '{AGENT_SPEECH_LANGUAGES[0]}', your language will depend on the type of interaction.

            - [1] If you are triggered by automated processes, default using English as a language.

            - [2] If you are triggered by a message from a live user, default using the language of the user's message.

        - If this part is EMPTY, your default language to respond will be English.

        ---
    """
