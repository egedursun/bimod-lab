#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: auto_command_prompts.py
#  Last Modified: 2024-10-16 01:34:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.core.drafting.drafting_executor import DraftingExecutionManager


def build_drafting_action__auto_prompt(xc: DraftingExecutionManager):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //auto
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [Your Internal Knowledge]
        - Tools You Have: [No Specific Tools Required]
        '''

        ---

        **YOUR GOAL:** The user picked the Auto-Completion Command action. You MUST check the user's text and
        understand the context very carefully. Then, you must provide an auto-completion for the rest of the text
        and ideally produce at least a few next sentences that are fitting to the overall status of the document.
        Do not make up information to complete the text, but rather use the existing information to generate the
        text or use your internal correct information to complete the text.

        ---

        **CURRENT DOCUMENT TEXT OF THE DOCUMENT:**

        '''
        {xc.drafting_document.document_content_json_quill}
        '''

    """
