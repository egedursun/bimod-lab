#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: repo_command_prompts.py
#  Last Modified: 2024-10-16 23:40:38
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 23:40:39
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_formica_action__repo_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //repo
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [CODE BASE REPOSITORY (VECTOR STORE) CONNECTIONS]
        - Tools Available: [USE CODE BASE REPOSITORY (VECTOR STORE) CONNECTIONS TO QUERY CODE FILES AND TEXT]
        '''

        ---

        **YOUR GOAL:** The user has selected the Code Base Repository / Vector Store Command action. Carefully review
        the user’s query to understand the type of information or assistance they need. Based on the query, perform a
        search in the Code Base Repository / Vector Store using the available connections. You may execute read-only
        commands to retrieve the information requested by the user. Use the data obtained from the repository to craft
        a response that aligns with the user's query and the form’s purpose. If the required information is available
        within your internal knowledge, you may skip the repository search, but ensure accuracy in all provided
        information.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
