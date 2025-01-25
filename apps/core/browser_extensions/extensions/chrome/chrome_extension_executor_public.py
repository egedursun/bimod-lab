#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: chrome_extension_executor_public.py
#  Last Modified: 2024-12-23 15:50:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-24 19:03:34
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

from apps.core.generative_ai.gpt_openai_manager import (
    OpenAIGPTClientManager
)

from apps.browser_extensions.models import (
    ChromeExtensionConnection
)

from apps.core.browser_extensions.extensions.chrome.public_handlers import (
    handle_ai_command_public,
    handle_nosql_command_public,
    handle_sql_command_public,
    handle_ssh_command_public,
    handle_vect_command_public,
    handle_web_command_public,
    handle_repo_command_public,
    handle_site_command_public,
)

logger = logging.getLogger(__name__)


class ExtensionExecutionManager_Public:

    def __init__(
        self,
        extension_google_apps_connection: ChromeExtensionConnection,
        text_content: str
    ):

        self.extension_connection = extension_google_apps_connection
        self.content = text_content
        self.copilot = extension_google_apps_connection.chrome_assistant
        self.copilot_llm = extension_google_apps_connection.chrome_assistant.llm_model

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
            output, error = handle_ai_command_public(
                xc=self,
                command=command,
                content=self.content
            )

            logger.info(
                f"[ExtensionExecutionManager_Public.handle_ai_command_public] AI command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_ai_command_public] Error executing AI command: {command}. Error: {e}")

            error = f"[ExtensionExecutionManager_Public.handle_ai_command_public] Error executing AI command: {command}. Error: {e}"

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
                f"[ExtensionExecutionManager_Public.handle_nosql_command_public] NOSQL command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_nosql_command_public] Error executing NOSQL command: {command}. Error: {e}")
            error = f"[ExtensionExecutionManager_Public.handle_nosql_command_public] Error executing NOSQL command: {command}. Error: {e}"

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
                f"[ExtensionExecutionManager_Public.handle_sql_command_public] SQL command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_sql_command_public] Error executing SQL command: {command}. Error: {e}")
            error = f"[ExtensionExecutionManager_Public.handle_sql_command_public] Error executing SQL command: {command}. Error: {e}"

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
                f"[ExtensionExecutionManager_Public.handle_ssh_command_public] SSH command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_ssh_command_public] Error executing SSH command: {command}. Error: {e}")
            error = f"[ExtensionExecutionManager_Public.handle_ssh_command_public] Error executing SSH command: {command}. Error: {e}"

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
                f"[ExtensionExecutionManager_Public.handle_vect_command_public] VECT command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_vect_command_public] Error executing VECT command: {command}. Error: {e}")
            error = f"[ExtensionExecutionManager_Public.handle_vect_command_public] Error executing VECT command: {command}. Error: {e}"

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
                f"[ExtensionExecutionManager_Public.handle_web_command_public] WEB command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_web_command_public] Error executing WEB command: {command}. Error: {e}")
            error = f"[ExtensionExecutionManager_Public.handle_web_command_public] Error executing WEB command: {command}. Error: {e}"

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
                f"[ExtensionExecutionManager_Public.handle_repo_command_public] REPO command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_repo_command_public] Error executing REPO command: {command}. Error: {e}")
            error = f"[ExtensionExecutionManager_Public.handle_repo_command_public] Error executing REPO command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error

        return response

    def execute_site_command(self, command: str):
        output, error = None, None

        response = {
            'output': output,
            'error': output
        }

        try:
            output, error = handle_site_command_public(
                xc=self,
                command=command,
                content=self.content
            )

            logger.info(
                f"[ExtensionExecutionManager_Public.handle_site_command_public] SITE command executed successfully: {command}")

        except Exception as e:
            logger.error(
                f"[ExtensionExecutionManager_Public.handle_site_command_public] Error executing SITE command: {command}. Error: {e}")
            error = f"[ExtensionExecutionManager_Public.handle_site_command_public] Error executing SITE command: {command}. Error: {e}"

        response['output'] = output
        response['error'] = error

        return response
