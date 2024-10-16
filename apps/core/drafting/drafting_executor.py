#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: drafting_executor.py
#  Last Modified: 2024-10-15 23:28:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-15 23:28:07
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager
from apps.drafting.models import DraftingDocument
from apps.core.drafting.handlers import (handle_ai_command, handle_auto_command, handle_img_command,
                                         handle_nosql_command, handle_select_command, handle_sql_command,
                                         handle_ssh_command, handle_vect_command, handle_web_command)


class DraftingExecutionManager:

    def __init__(self, drafting_document: DraftingDocument):
        self.drafting_document = drafting_document
        self.copilot = drafting_document.copilot_assistant
        self.copilot_llm = drafting_document.copilot_assistant.llm_model
        self.naked_c = OpenAIGPTClientManager.get_naked_client(llm_model=self.copilot_llm)
        self._build_prompt()

    def _build_prompt(self):
        self.generic_prompt = f"TODO: Not implemented yet. DraftingExecutionManager._build_prompt()"
        self.command_specific_prompt = f"TODO: Not implemented yet. DraftingExecutionManager._build_prompt()"
        self.data_source_prompt = f"TODO: Not implemented yet. DraftingExecutionManager._build_prompt()"
        self.tool_execution_prompt = f"TODO: Not implemented yet. DraftingExecutionManager._build_prompt()"

    #####

    def execute_ai_command(self, command: str):
        try:
            output: str = handle_ai_command(command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_ai_command] Error executing AI command: {command}. Error: {e}"
        return output

    def execute_auto_command(self):
        try:
            output: str = handle_auto_command()
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_auto_command] Error executing AUTO command: {command}. Error: {e}"
        return output

    def execute_img_command(self, command: str):
        try:
            output: str = handle_img_command(command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_img_command] Error executing IMG command: {command}. Error: {e}"
        return output

    def execute_nosql_command(self, command: str):
        try:
            output: str = handle_nosql_command(command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_nosql_command] Error executing NOSQL command: {command}. Error: {e}"
        return output

    def execute_select_command(self, selected_text: str, command: str):
        try:
            output: str = handle_select_command(selected_text=selected_text, command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_select_command] Error executing SELECT command: {command}. Error: {e}"
        return output

    def execute_sql_command(self, command: str):
        try:
            output: str = handle_sql_command(command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_sql_command] Error executing SQL command: {command}. Error: {e}"
        return output

    def execute_ssh_command(self, command: str):
        try:
            output: str = handle_ssh_command(command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_ssh_command] Error executing SSH command: {command}. Error: {e}"
        return output

    def execute_vect_command(self, command: str):
        try:
            output: str = handle_vect_command(command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_vect_command] Error executing VECT command: {command}. Error: {e}"
        return output

    def execute_web_command(self, command: str):
        try:
            output: str = handle_web_command(command=command)
        except Exception as e:
            output = f"[DraftingExecutionManager.execute_web_command] Error executing WEB command: {command}. Error: {e}"
        return output
