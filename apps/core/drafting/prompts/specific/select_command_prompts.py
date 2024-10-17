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

def build_drafting_action__select_prompt(user_query: str, selected_text: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //select
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [Your Internal Knowledge]
        - Tools You Have: [No Specific Tools Required]
        '''

        ---

        **YOUR GOAL:** The user picked the Selection Modifier Command action. You MUST check the user's query and
        understand what kind of modification they want to perform on the text. Then, you must modify the text user
        selected in a way to satisfy his expectations and needs. The content must be fitting the overall status of the
        document, the query of the user, and of course only modify the selected text.

        ---

        **SELECTED TEXT:**

        '''
        {selected_text}
        '''

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
