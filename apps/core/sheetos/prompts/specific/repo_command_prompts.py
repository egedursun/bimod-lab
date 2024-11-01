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


def build_sheetos_action__repo_prompt(user_query: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //repo
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [CODE BASE REPOSITORY (VECTOR STORE) CONNECTIONS]
        - Tools You Have: [USE CODE BASE REPOSITORY (VECTOR STORE) CONNECTIONS TO QUERY CODE FILES AND TEXT]
        '''

        ---

        **YOUR GOAL:** The user picked the Code Base Repository / Vector Store Command action. You MUST check the user's
        query and understand what kind of operation they want to perform. And then, based on the query they provided
        to you, you need to perform a search on the Code Base Repository / Vector Store using one of the available Code
        Base Repository / Vector Store connections you have. You can run any type of read Knowledge Base / Vector Store
        command on the vector store to get the information requested by the user. Then, using the information you found
        in the vector store, you must generate the plain CSV-formatted data in a shape and content requested by the
        user's query. If you have the information specified in your own internal knowledge, you don't need to perform
        a Code Base Repository / Vector Store search. But be careful in not providing false information (unless
        specifically requested by the user). Always share your results in plain CSV format.

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
