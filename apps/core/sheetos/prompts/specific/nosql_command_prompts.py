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

def build_sheetos_action__nosql_prompt(user_query: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //nosql
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [NoSQL DATABASE CONNECTIONS]
        - Tools You Have: [USE NoSQL DATABASE CONNECTIONS TO EXECUTE NoSQL READ QUERIES]
        '''

        ---

        **YOUR GOAL:** The user picked the NoSQL Command action. You MUST check the user's query and understand what
        kind of operation they want to perform. And then, based on the query they provided to you, you need to perform
        a search on the NoSQL database using one of the available NoSQL database connections you have. You can run any
        type of read NoSQL (**ONLY N1QL IS SUPPORTED**) query on the database to get the information requested by the
        user. Then, using the information you found in the database, you must generate the data in the plain CSV format
        fitting into the requested principles within the user's query. If you have the information specified in your
        own internal knowledge, you don't need to perform a database search. But be careful in not providing false
        information (unless specifically requested by the user). Always share your results in plain CSV format.

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
