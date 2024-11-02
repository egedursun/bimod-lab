#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sql_command_prompts.py
#  Last Modified: 2024-10-16 01:35:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-16 01:35:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_formica_action__sql_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //sql
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [SQL DATABASE CONNECTIONS]
        - Tools Available: [USE SQL DATABASE CONNECTIONS TO EXECUTE SQL READ QUERIES]
        '''

        ---

        **YOUR GOAL:** The user has selected the SQL Command action. Review the user’s query to understand the specific
        data they need. Based on the query, perform a search on the SQL database using the available SQL database
        connections. You may execute any read-only SQL query to retrieve the required information. Use the data obtained
        to craft a response that aligns with the user’s query and the form’s purpose. If the information is already
        available in your internal knowledge, you may skip the database search, but ensure accuracy in all provided
        information.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
