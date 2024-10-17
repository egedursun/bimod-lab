#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#

def build_drafting_action__sql_prompt(user_query: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //sql
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [SQL DATABASE CONNECTIONS]
        - Tools You Have: [USE SQL DATABASE CONNECTIONS TO EXECUTE SQL READ QUERIES]
        '''

        ---

        **YOUR GOAL:** The user picked the SQL Command action. You MUST check the user's query and understand what
        kind of operation they want to perform. And then, based on the query they provided to you, you need to perform
        a search on the SQL database using one of the available SQL database connections you have. You can run any type
        of read SQL query on the database to get the information requested by the user. Then, using the information
        you found in the database, you must write the text in the form and content requested by the user's query. If you
        have the information specified in your own internal knowledge, you don't need to perform a database search. But
        be careful in not providing false information (unless specifically requested by the user).

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
