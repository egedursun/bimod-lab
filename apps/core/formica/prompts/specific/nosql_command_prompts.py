#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: nosql_command_prompts.py
#  Last Modified: 2024-10-16 01:35:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_formica_action__nosql_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //nosql
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [NoSQL DATABASE CONNECTIONS]
        - Tools Available: [USE NoSQL DATABASE CONNECTIONS TO EXECUTE NoSQL READ QUERIES]
        '''

        ---

        **YOUR GOAL:** The user has selected the NoSQL Command action. Carefully review the user’s query to understand
        the type of information they need. Based on the query, perform a search on the NoSQL database using the available
        NoSQL database connections. You may execute read-only NoSQL queries (**ONLY N1QL IS SUPPORTED**) to retrieve
        the requested information. Use the data found in the database to craft a response that aligns with the user’s
        query and the form’s context. If the required information is available within your internal knowledge, you may
        skip the database search, but ensure accuracy in all provided information.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
