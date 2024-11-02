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

def build_formica_action__ssh_prompt(user_query: str) -> str:
    return f"""
        ### **USER SELECTED ACTION:**

        '''
            //ssh
        '''

        **Tools & Data Sources:**

        '''
        - Data Sources Available: [SSH FILE SYSTEM CONNECTIONS]
        - Tools Available: [USE SSH FILE SYSTEM CONNECTIONS TO EXECUTE SSH FILE SYSTEM READ QUERIES]
        '''

        ---

        **YOUR GOAL:** The user has selected the SSH File System Command action. Carefully review the user’s query
        to understand the specific information they need. Based on the query, perform a search on the SSH File System
        using the available connections. Execute any read-only SSH command necessary to retrieve the requested data.
        Use the information obtained from the file system to provide a response that aligns with the user's query and
        the purpose of the form. If the information is available within your internal knowledge, you may skip the SSH
        file system search, but ensure that all information provided is accurate.

        ---

        **USER QUERY:**

        '''
        {user_query}
        '''
    """
