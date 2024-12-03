#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: file_systems_executor.py
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

import json
import logging

import paramiko

from apps.core.file_systems.utils import DEFAULT_BANNER_TIMEOUT
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts

from apps.core.file_systems.internal_command_sets import (
    INTERNAL_COMMAND_SETS,
    LIST_DIRECTORY_RECURSIVE
)

from paramiko import SSHClient
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames

logger = logging.getLogger(__name__)


class FileSystemsExecutor:
    def __init__(self, connection):
        self.connection = connection
        self.client = None
        self.connect_c()
        self.schema_str = self.retrieve_file_tree_schema()

    def connect_c(self):
        try:
            ssh_connection_host = self.connection.host_url
            ssh_port = self.connection.port
            ssh_username = self.connection.username
            ssh_password = self.connection.password
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                ssh_connection_host,
                port=ssh_port,
                username=ssh_username,
                password=ssh_password,
                banner_timeout=DEFAULT_BANNER_TIMEOUT
            )
            self.client = ssh
            logger.info(f"Connected to the remote host: {ssh_connection_host}")

        except Exception as e:
            logger.error(f"Failed to connect to the remote host: {e}")
            pass

        return self.client

    def close_c(self):
        try:
            self.client.stdin.close()
            self.client.stdout.close()
            self.client.stderr.close()
            self.client.ssh.close()
            logger.info(f"Closed the connection to the remote host: {self.connection.host_url}")

        except Exception as e:
            logger.error(f"Failed to close the connection to the remote host: {e}")
            pass

        return

    def parse_ls_r_output(
        self,
        output,
        max_depth=3
    ):
        try:
            lines = output.strip().split('\n')
            root = {}
            current_dir = root
            dir_stack = [root]
            depth_stack = [0]

            for line in lines:

                if line.endswith(':'):
                    current_path = line[:-1]
                    dirs = current_path.split('/')

                    if current_path.startswith('.'):
                        current_dir = root
                        current_depth = 0

                        for d in dirs[1:]:
                            if current_depth < max_depth:
                                current_dir = current_dir.setdefault(d, {})
                                current_depth += 1

                            else:
                                current_dir['<deeper_than:{}>'.format(max_depth)] = {}
                                break
                        pass

                        dir_stack = dir_stack[:len(dirs)]
                        depth_stack = depth_stack[:len(dirs)]
                        dir_stack.append(current_dir)
                        depth_stack.append(current_depth)

                    else:
                        current_dir = dir_stack[-1]

                else:

                    if line:
                        current_depth = depth_stack[-1]

                        if current_depth < max_depth:
                            current_dir[line] = {}

                        else:
                            current_dir['<deeper_than:{}-levels>'.format(max_depth)] = {}

                    else:
                        pass

            pass
            logger.info(f"Parsed the file tree schema: {root}")

        except Exception as e:
            logger.error(f"Failed to parse the file tree schema: {e}")
            return {}

        return root

    def retrieve_file_tree_schema(self):
        client = self.connect_c()

        try:
            query = INTERNAL_COMMAND_SETS[LIST_DIRECTORY_RECURSIVE][self.connection.os_type]
            stdin, stdout, stderr = client.exec_command(query)
            file_directory_tree = stdout.read().decode()

            directory_dict = json.dumps(
                self.parse_ls_r_output(
                    file_directory_tree
                ),
                default=str
            )

            directory_dict = directory_dict[:int(self.connection.os_read_limit_tokens)] if (
                len(directory_dict) > int(self.connection.os_read_limit_tokens)) else directory_dict

            logger.info(f"Retrieved the file tree schema: {directory_dict}")

        except Exception as e:
            logger.error(f"Failed to retrieve the file tree schema: {e}")
            directory_dict = "{}"

        self.close_c()
        return directory_dict

    def execute_file_system_command_set(self, commands: list[str]):

        from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps.core.generative_ai.utils import ChatRoles

        client = self.connect_c()

        results = {
            "status": True,
            "stdins": [],
            "stdouts": [],
            "stderrs": [],
            "schema_before_execution": self.schema_str,
            "updated_schema": ""
        }

        for i, command in enumerate(commands):

            try:
                stdin, stdout, stderr = client.exec_command(command)
                results["stdins"].append(command)
                results["stdouts"].append(stdout.read().decode())
                results["stderrs"].append(stderr.read().decode())
                logger.info(f"Executed the command: {command}")

            except Exception as e:
                results["status"] = False
                results["stdins"].append(command)
                results["stdouts"].append(f"Error executing the command: {str(e)}")
                results["stderrs"].append("")
                logger.error(f"Failed to execute the command: {command}")

        try:
            updated_schema = self.retrieve_file_tree_schema()
            results["updated_schema"] = updated_schema
            self.close_c()
            logger.info(f"Updated the file tree schema: {updated_schema}")

        except Exception as e:
            logger.error(f"Failed to update the file tree schema: {e}")
            pass

        try:
            tx = LLMTransaction(
                organization=self.connection.assistant.organization,
                model=self.connection.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=InternalServiceCosts.FileSystemsExecutor.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.FILE_SYSTEM_COMMANDS,
                is_tool_cost=True
            )

            tx.save()
            logger.info(f"Created a new LLM transaction for the file system command execution: {tx}")

        except Exception as e:
            logger.error(f"Failed to create a new LLM transaction for the file system command execution: {e}")
            pass

        return results
