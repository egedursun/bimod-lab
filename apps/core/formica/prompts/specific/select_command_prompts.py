#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: select_command_prompts.py
#  Last Modified: 2024-10-16 01:35:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_formica_action__select_prompt(user_query: str, selected_text: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //select
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [Your Internal Knowledge]
        - Tools Available: [No Specific Tools Required]
        '''

        ---

        **YOUR GOAL:** The user has selected the Selection Modifier Command action. Carefully review the user’s query
        to understand the specific modification they want to apply to the selected text in the form. Your task is to
        adjust the selected text in a way that aligns with the user's requirements while fitting the overall purpose
        of the form. Only modify the provided selected text.

        ---

        **SELECTED TEXT:**

        '''
        {selected_text}
        '''

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
