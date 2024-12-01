#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_expert_network_to_assistant_instructions_prompt.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


def build_leanmod_to_expert_assistant_instructions_prompt(query_text: str) -> str:
    return f"""
        **WARNING: This is an automated message.**

            *IMPORTANT*: PLEASE READ FOLLOWING NOTE CAREFULLY !
            ---
            YOUR SUBJECT IS 'NOT' A HUMAN. IT 'IS' AN AI LIKE YOU.
            ---

            - If you see this, it means this message is sent to you by LEANMOD ORCHESTRATOR assistant,
            within context of complex task execution. Please know that respondent to your messages is NOT
            human; instead an AI system like you. The orchestrator is tasked for coordinating execution of
            complex tasks requiring multiple tools/capabilities that can be done by multiple assistants.
            Thus, do not expect understanding whole picture of what orchestrator wants. Instead, please
            DO YOUR BEST to accomplish described task based on your tools/capabilities, and leave rest
            to be handled by orchestrator.

            NEVER decline task given by orchestrator. If you are unable to complete, please inform
            orchestrator assistant, so that it can take actions to complete task. Yet, if you have capability
            to accomplish task, even if you are not 100% sure, DO YOUR BEST to complete.

            - If you have questions or need clarity about task, ask orchestrator. Yet, don't ask questions
            that are not essential to complete the task. Only ask questions about blockers preventing you from
            completion, and wait for orchestrator to respond with info.

            ---

            Orchestrator's Message:

            ```
            {query_text}
            ```

            ---
    """
