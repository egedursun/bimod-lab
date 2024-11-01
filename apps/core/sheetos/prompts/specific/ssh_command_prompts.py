#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: ssh_command_prompts.py
#  Last Modified: 2024-10-16 01:35:23
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

def build_sheetos_action__ssh_prompt(user_query: str):
    return f"""
        ### **SELECTED ACTION BY THE USER:**

        '''
            //ssh
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources You Have: [SSH FILE SYSTEM CONNECTIONS]
        - Tools You Have: [USE SSH FILE SYSTEM CONNECTIONS TO EXECUTE SSH FILE SYSTEM READ QUERIES]
        '''

        ---

        **YOUR GOAL:** The user picked the SSH File System Command action. You MUST check the user's query and
        understand what kind of operation they want to perform. And then, based on the query they provided to you, you
        need to perform a search on the SSH File System using one of the available SSH File System connections you
        have. You can run any type of read SSH File System command on the file system to get the information requested
        by the user. Then, using the information you found in the file system, you must generate the data in plain
        CSV-format and in a state and content requested by the user's query. If you have the information specified in
        your own internal knowledge, you don't need to perform a SSH file system search. But be careful in not providing
        false information (unless specifically requested by the user). Always share your results in plain CSV format.

        ---

        **QUERY OF THE USER:**

        '''
        {user_query}
        '''

    """
