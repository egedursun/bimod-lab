#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: site_command_prompts.py
#  Last Modified: 2024-12-09 18:45:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 18:45:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_drafting_action__site_prompt(user_query: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //site
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [WEBSITE STORAGE (VECTOR STORE) CONNECTIONS]
        - Tools You Have: [USE WEBSITE STORAGE (VECTOR STORE) CONNECTIONS TO QUERY PREVIOUSLY INDEXED WEBSITE DATA]
        '''

        ---

        **YOUR GOAL:** The user picked the Website Storage Connection action. You MUST check the user's
        query and understand what kind of operation they want to perform. And then, based on the query they provided
        to you, you need to perform a search on the specified website URL (or if no URL is provided, leave the website
        URL field empty to query ALL website storage, using one of the available Website storage connections you have.
        You can run any type of query on the website data vector store to get the information requested by the user. Then,
        using the information you found in the website data vector store's chunks related to the previously indexed website
        data, you must write the text in the form and content requested by the user's query. If you have the information
        specified in your own internal knowledge, you don't need to perform a Website Data Storage search. But be careful
        in not providing false information (unless specifically requested by the user).

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
