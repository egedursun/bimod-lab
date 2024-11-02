#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ai_command_prompts.py
#  Last Modified: 2024-10-16 01:34:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_formica_action__ai_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //ai
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [Your Internal Knowledge]
        - Tools Available: [No Specific Tools Required]
        '''

        ---

        **YOUR GOAL:** The user has selected the AI Command action. You MUST review the user's query to understand
        what kind of assistance they seek with the form content. Then, create a response that aligns with the purpose
        of the form and addresses the user's needs. There is no strict length limit, but avoid making it excessively
        long.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
