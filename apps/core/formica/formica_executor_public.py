#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: formica_executor_public.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 13:16:31
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
from apps.core.formica.public_handlers import (handle_ai_command_public, handle_auto_command_public,
                                               handle_img_command_public, handle_nosql_command_public,
                                               handle_select_command_public, handle_sql_command_public,
                                               handle_ssh_command_public, handle_vect_command_public,
                                               handle_web_command_public, handle_repo_command_public)
from apps.formica.models import FormicaGoogleAppsConnection

logger = logging.getLogger(__name__)


class FormicaExecutionManager_Public:

    def __init__(
        self,
        formica_google_apps_connection: FormicaGoogleAppsConnection,
        text_content: str
    ):

        self.document_connection = formica_google_apps_connection
        self.content = text_content
        self.copilot = formica_google_apps_connection.formica_assistant
        self.copilot_llm = formica_google_apps_connection.formica_assistant.llm_model
        self.naked_c = OpenAIGPTClientManager.get_naked_client(
            llm_model=self.copilot_llm
        )

    #####

    def execute_ai_command(
        self,
        command: str
    ):

        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_ai_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_ai_command_public] AI command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_ai_command_public] Error executing AI command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_ai_command_public] Error executing AI command: {command}. Error: {e}"

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
            output, error = handle_auto_command_public(
                xc=self,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_auto_command_public] AUTO command executed successfully.")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_auto_command_public] Error executing AUTO command. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_auto_command_public] Error executing AUTO command. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_img_command(self, command: str):
        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_img_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_img_command_public] IMG command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_img_command_public] Error executing IMG command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_img_command_public] Error executing IMG command: {command}. Error: {e}"

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
            output, error = handle_nosql_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_nosql_command_public] NOSQL command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_nosql_command_public] Error executing NOSQL command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_nosql_command_public] Error executing NOSQL command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response

    def execute_select_command(
        self,
        selected_text: str,
        command: str
    ):

        output, error = None, None
        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_select_command_public(
                xc=self,
                selected_text=selected_text,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_select_command_public] SELECT command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_select_command_public] Error executing SELECT command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_select_command_public] Error executing SELECT command: {command}. Error: {e}"

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
            output, error = handle_sql_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_sql_command_public] SQL command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_sql_command_public] Error executing SQL command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_sql_command_public] Error executing SQL command: {command}. Error: {e}"

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
            output, error = handle_ssh_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_ssh_command_public] SSH command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_ssh_command_public] Error executing SSH command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_ssh_command_public] Error executing SSH command: {command}. Error: {e}"

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
            output, error = handle_vect_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_vect_command_public] VECT command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_vect_command_public] Error executing VECT command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_vect_command_public] Error executing VECT command: {command}. Error: {e}"

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
            output, error = handle_web_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_web_command_public] WEB command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_web_command_public] Error executing WEB command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_web_command_public] Error executing WEB command: {command}. Error: {e}"

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
            output, error = handle_repo_command_public(
                xc=self,
                command=command,
                content=self.content
            )
            logger.info(
                f"[FormicaExecutionManager_Public.handle_repo_command_public] REPO command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[FormicaExecutionManager_Public.handle_repo_command_public] Error executing REPO command: {command}. Error: {e}")
            error = f"[FormicaExecutionManager_Public.handle_repo_command_public] Error executing REPO command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error
        return response
