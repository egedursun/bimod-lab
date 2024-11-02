#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: vect_command_prompts.py
#  Last Modified: 2024-10-16 01:35:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_formica_action__vect_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //vect
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [KNOWLEDGE BASE (VECTOR STORE) CONNECTIONS]
        - Tools Available: [USE KNOWLEDGE BASE (VECTOR STORE) CONNECTIONS TO QUERY DOCUMENTS AND TEXT]
        '''

        ---

        **YOUR GOAL:** The user has selected the Knowledge Base / Vector Store Command action. Carefully review the
        user’s query to understand the specific information they are seeking. Based on the query, perform a search
        on the Knowledge Base / Vector Store using the available connections. Execute any necessary read-only commands
        to retrieve relevant information. Use the data obtained to provide a response that aligns with the user’s
        query and the form’s purpose. If the required information is already available within your internal knowledge,
        you may skip the vector store search, but ensure all information provided is accurate.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
