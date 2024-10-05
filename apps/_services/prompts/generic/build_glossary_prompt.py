#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: build_glossary_prompt.py
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

def build_structured_glossary_prompt(glossary: str):
    return f"""
        **YOUR GLOSSARY AND TERMINOLOGY:**

        '''
        {glossary}
        '''

        **NOTE**: This is the glossary and terminology that you will be aware of to understand the internal
        language and jargon of the organizations and domains. Make sure to keep this in mind while preparing
        the responses for the user's messages. If this part is EMPTY, you can use the general terminology that
        you are aware of.
    """
