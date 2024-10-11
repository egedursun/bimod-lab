#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: json_operation_prompts.py
#  Last Modified: 2024-10-08 23:49:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 23:49:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


def get_maximum_tool_chains_reached_log(final_response: str):
    log = f"""
        {final_response}

        ---

        System Message:

        The maximum number of multiple tool chains is reached. No further chaining can be executed. If you believe
        you need to be able to chain more tools together, please increase the limit in the agent settings.

        The response generation cycle is going to be stopped now.

        ---

    """
    return log


def get_maximum_tool_attempts_reached_log(final_response: str):
    log = f"""
        {final_response}

        ---

        System Message:

        The maximum number of attempts for this tool has been reached. No further attempts can be made
        for retrieval via this tool. If you believe you need to be able to make more attempts for using the same
        tool, please increase the limit in the agent settings.

        The response generation cycle is going to be stopped now.

        ---
    """
    return log


def embed_tool_call_in_prompt(json_parts_of_response: str):
    prompt = f"""
    **Assistant Tool Call:**

    ```

    {json_parts_of_response}

    ```

    ---
    """
    return prompt
