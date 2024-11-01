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


def build_sheetos_action__ai_prompt(user_query: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //ai
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [Your Internal Knowledge]
        - Tools You Have: [No Specific Tools Required]
        '''

        ---

        **YOUR GOAL:** The user picked the AI Command action. You MUST check the user's query and understand what
        kind of operation they want to perform on the spreadsheet. Then, you must generate data that's fitting the
        overall status of the spreadsheet document, as well as the query of the user to satisfy his expectations and
        needs. There is no upper or lower in the limit in the data you generate as long as it doesnt pass your context
        window limitations. Always share your results in plain CSV format.

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
