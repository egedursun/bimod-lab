#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: build_response_language_prompt.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: build_response_language_prompt.py
#  Last Modified: 2024-08-01 13:09:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:10:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

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
