#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sheetos_executor.py
#  Last Modified: 2024-10-31 20:46:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 22:05:47
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from apps.core.generative_ai.gpt_openai_manager import OpenAIGPTClientManager

from apps.core.sheetos.handlers import (
    handle_ai_command,
    handle_auto_command,
    handle_nosql_command,
    handle_select_command,
    handle_sql_command,
    handle_ssh_command,
    handle_vect_command,
    handle_web_command,
    handle_repo_command
)

from apps.sheetos.models import SheetosDocument

logger = logging.getLogger(__name__)


class SheetosExecutionManager:

    def __init__(self, sheetos_document: SheetosDocument):
        self.sheetos_document = sheetos_document
        self.copilot = sheetos_document.copilot_assistant
        self.copilot_llm = sheetos_document.copilot_assistant.llm_model
        self.naked_c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.copilot_llm
        )

    #####

    def execute_ai_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_ai_command(xc=self, command=command)
            logger.info(f"[SheetosExecutionManager.execute_ai_command] AI command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_ai_command] Error executing AI command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_ai_command] Error executing AI command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_auto_command(self):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_auto_command(xc=self)
            logger.info(f"[SheetosExecutionManager.execute_auto_command] AUTO command executed successfully.")

        except Exception as e:
            logger.error(f"[SheetosExecutionManager.execute_auto_command] Error executing AUTO command. Error: {e}")
            error = f"[SheetosExecutionManager.execute_auto_command] Error executing AUTO command. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_nosql_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_nosql_command(xc=self, command=command)
            logger.info(
                f"[SheetosExecutionManager.execute_nosql_command] NOSQL command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_nosql_command] Error executing NOSQL command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_nosql_command] Error executing NOSQL command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_select_command(self, selected_data: str, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_select_command(
                xc=self,
                selected_data=selected_data,
                command=command
            )
            logger.info(
                f"[SheetosExecutionManager.execute_select_command] SELECT command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_select_command] Error executing SELECT command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_select_command] Error executing SELECT command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_sql_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_sql_command(xc=self, command=command)
            logger.info(f"[SheetosExecutionManager.execute_sql_command] SQL command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_sql_command] Error executing SQL command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_sql_command] Error executing SQL command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_ssh_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_ssh_command(xc=self, command=command)
            logger.info(f"[SheetosExecutionManager.execute_ssh_command] SSH command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_ssh_command] Error executing SSH command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_ssh_command] Error executing SSH command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_vect_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_vect_command(xc=self, command=command)
            logger.info(
                f"[SheetosExecutionManager.execute_vect_command] VECT command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_vect_command] Error executing VECT command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_vect_command] Error executing VECT command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_web_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_web_command(xc=self, command=command)
            logger.info(f"[SheetosExecutionManager.execute_web_command] WEB command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_web_command] Error executing WEB command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_web_command] Error executing WEB command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_repo_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_repo_command(xc=self, command=command)
            logger.info(
                f"[SheetosExecutionManager.execute_repo_command] REPO command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[SheetosExecutionManager.execute_repo_command] Error executing REPO command: {command}. Error: {e}")
            error = f"[SheetosExecutionManager.execute_repo_command] Error executing REPO command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response
