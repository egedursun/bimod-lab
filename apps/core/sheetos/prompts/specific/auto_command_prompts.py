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
from apps.core.sheetos.sheetos_executor import SheetosExecutionManager


def build_sheetos_action__auto_prompt(xc: SheetosExecutionManager):
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

        **YOUR GOAL:** The user picked the Auto-Completion Command action. You MUST check the user's spreadsheet content
        and understand the context very carefully. Then, you must provide an auto-completion for the rest of the data
        and ideally produce at least a few next rows of data that are fitting to the overall status of the spreadsheet
        document. Rather use the existing information to generate the data in CSV format, or use your internal correct
        information to complete the data. Always share your results in plain CSV format.

        ---

        **CURRENT CONTENT OF THE SPREADSHEET DOCUMENT:**

        '''
        {xc.sheetos_document.document_content_json_quill}
        '''

    """


def build_sheetos_action__auto_prompt_public(content: str):
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

        **YOUR GOAL:** The user picked the Auto-Completion Command action. You MUST check the user's spreadsheet content
        and understand the context very carefully. Then, you must provide an auto-completion for the rest of the data
        and ideally produce at least a few next rows of data that are fitting to the overall status of the spreadsheet
        document. Rather use the existing information to generate the data in CSV format, or use your internal correct
        information to complete the data. Always share your results in plain CSV format.

        ---

        **CURRENT CONTENT OF THE SPREADSHEET DOCUMENT:**

        '''
        {content}
        '''

    """
