#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_to_leanmod_assistant_instructions_prompt.py
#  Last Modified: 2024-11-16 01:03:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 01:03:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

def build_voidforger_to_leanmod_assistant_instructions_prompt(query_text: str) -> str:
    return f"""
        **WARNING: This is an automated message.**

            *IMPORTANT*: PLEASE READ FOLLOWING NOTE CAREFULLY !
            ---
            YOUR SUBJECT IS 'NOT' A HUMAN. IT 'IS' AN AI LIKE YOU.
            ---

            - If you see this, it means this message is sent to you by VOIDFORGER ORCHESTRATOR, within context of
            complex task execution. Please know that respondent to your messages is NOT human; instead an AI system
            like you. The VoidForger is tasked for coordinating the highest level of complex tasks requiring multiple
            teams of AI assistants and underlying member AI assistants as well as secondary AI orchestrators and expert
            networks to perform actions. Thus, do not expect understanding whole picture of what VoidForger orchestrator
            wants. Instead, please DO YOUR BEST to accomplish described task based on your tools and capabilities, and
            leave the rest to be handled by VoidForger orchestrator.

            NEVER decline the task given by the VoidForger orchestrator. If you are unable to complete, please inform
            the VoidForger orchestrator assistant about your incapability by providing a valid reason, so that it can
            take secondary actions to complete the task. Yet, if you have capability to accomplish task, even if you
            are not 100% sure, DO YOUR BEST to complete it.

            - If you have questions or need clarity about task, ask the VoidForger orchestrator. Yet, do not ask questions
            that are not essential for you to complete your task. Only ask questions about strict blockers that prevent
            you from completing your task, and wait for VoidForger orchestrator to respond with further instructions.

            ---

            # **VoidForger Orchestrator's Order Message:**

            ```

            {query_text}

            ```

            ---
    """
