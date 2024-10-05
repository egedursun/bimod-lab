#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_response_language_prompt.py
#  Last Modified: 2024-10-05 02:25:59
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
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

from apps.assistants.models import ASSISTANT_RESPONSE_LANGUAGES


def build_structured_response_language_prompt(response_language: str):
    return f"""
        **YOUR RESPONSE LANGUAGE:**

        '''
        {response_language}
        '''

        **NOTE**: This is the language that you will be using while responding to the user's messages. If this
        part is named {ASSISTANT_RESPONSE_LANGUAGES[0]}, you MUST respond in the language the user is asking
        you the questions. If this part is EMPTY, your default language to respond to the user's messages will
        be English.
    """
