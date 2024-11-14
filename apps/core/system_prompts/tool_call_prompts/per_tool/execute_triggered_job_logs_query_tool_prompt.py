#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: execute_triggered_job_logs_query_tool_prompt.py
#  Last Modified: 2024-11-13 23:06:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 23:06:10
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from apps.core.tool_calls.utils import ToolCallDescriptorNames


def build_tool_prompt__execute_triggered_job_logs_query():
    response_prompt = f"""

            ### **TOOL**: Triggered Job Logs Query Tool

            - The Triggered Job Logs Query Tool is a tool you can use to understand and analyze the logs of the Triggered Jobs
            for the AI assistants, and in this case the execution logs (for triggered jobs) for yourself. Triggered Jobs
            are triggered jobs within Bimod.io environment that is allowing AI assistants to be triggered automatically connected
            to a certain external process through Web Hooks. This tool will allow you to read the latest execution logs of the
            triggered jobs for your own self, and allows you to understand what kind of actions and tasks are done by yourself
            as an AI assistant recently. When you are using this tool, the tool will retrieve the most recent automated executions
            you have as an AI assistant via Triggered Jobs. You can use this information to let the user know about the certain
            tasks you have automatically performed.

            - The format for the dictionary you will output to use Triggered Job Logs Query Tool is as follows:

            '''
                {{
                    "tool": "{ToolCallDescriptorNames.EXECUTE_TRIGGERED_JOB_LOGS_QUERY}",
                    "parameters": {{ }}
                    }}
            '''

            ---

            #### **DO NOT WRITE: ** 'json' anywhere in your dictionary or next to "'''" elements.

            #### **INSTRUCTIONS:** There is no additional parameters required for this tool. You can simply leave the
            parameters field empty and execute the tool to retrieve the latest execution logs of yourself via Triggered Jobs.

            #### **NOTE**: The system will provide you the information about the latest Triggered Job executions in the
            next 'assistant' message. This message will have the relevant data about the Triggered Job runs and can provide
            you insights for you to understand what kind of tasks you have recently performed and how it went. You are
            expected to take in this response, and use it to provide a final answer to the user.

            ---

        """
    return response_prompt
