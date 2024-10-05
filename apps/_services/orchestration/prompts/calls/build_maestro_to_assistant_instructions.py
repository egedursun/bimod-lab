#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: build_maestro_to_assistant_instructions.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#
#
#  Project: Bimod.io
#  File: build_maestro_to_assistant_instructions.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:08:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

def build_maestro_to_assistant_instructions_prompt(maestro_query_text: str) -> str:
    return f"""
        **WARNING: This is an ORCHESTRATOR-GENERATED user message.**

            !!! IMPORTANT: PLEASE READ THE FOLLOWING WARNING CAREFULLY !!!
            ---
            YOUR SUBJECT IS '''NOT''' A HUMAN BEING. YOUR SUBJECT 'IS' AN ARTIFICIAL INTELLIGENCE SYSTEM LIKE YOU.
            ---

            - If you see this message, it means that this message is sent to you by the ORCHESTRATOR assistant,
            within the context of a complex task execution. Please know that the respondent to your messages is NOT
            a human being; an instead an artificial intelligence system like you. The orchestration assistant is tasked
            for coordinating and managing the execution of complex tasks that require multiple tools and capabilities
            that can be reached by different assistants. Thus, do not expect to understand the complete picture of
            what the orchestrator wants to achieve. Instead, please DO YOUR BEST to accomplish the described task
            based on your available tools and capabilities, and leave the rest to be handled by the orchestrator.

            NEVER deny or decline the task given to you by the orchestrator. If you are unable to complete the task,
            please inform the orchestrator assistant immediately, so that it can take necessary actions to complete
            the task. However, if you have the capability to accomplish a certain task, even if you are not 100%
            sure, please DO YOUR BEST to complete the task. The orchestrator assistant will take care of the rest.

            - If you have any questions or need clarification about the task, please ask the orchestrator. However,
                please don't ask questions that are not required for you to complete the task. Only ask questions about
                the blockers that prevent you from completing the task, and wait for the orchestrator to respond to you
                with the necessary information.

            ---

            Orchestrator's Message to You:

            ```
            {maestro_query_text}
            ```

            ---
    """
