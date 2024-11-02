#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: web_command_prompts.py
#  Last Modified: 2024-10-16 01:35:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_formica_action__web_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //web
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [BROWSER CONNECTIONS]
        - Tools Available: [USE BROWSER TOOLS TO EXECUTE WEB SEARCHES]
        '''

        ---

        **YOUR GOAL:** The user has selected the Web Command action. Carefully review the user’s query to understand
        the specific information they need. Based on the query, perform a web search using the available browser
        connections. Use the information found online to craft a response that aligns with the user’s query and the
        form’s purpose. If the information is already available within your internal knowledge, you may skip the
        web search, but ensure accuracy in all provided information.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
