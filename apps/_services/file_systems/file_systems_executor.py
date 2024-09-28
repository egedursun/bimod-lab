import json
import paramiko
from apps._services.config.costs_map import ToolCostsMap
from apps._services.file_systems.internal_command_sets import INTERNAL_COMMAND_SETS, LIST_DIRECTORY_RECURSIVE
from paramiko import SSHClient
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import TransactionSourcesNames


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
            ssh.connect(ssh_connection_host, port=ssh_port, username=ssh_username, password=ssh_password,
                        banner_timeout=200)
            print(f"[FileSystemsExecutor.connect_c] Connected to SSH successfully.")
            self.client = ssh
        except Exception as e:
            print(f"[FileSystemsExecutor.connect_c] Error connecting to SSH: {e}")
        return self.client

    def close_c(self):
        try:
            self.client.stdin.close()
            self.client.stdout.close()
            self.client.stderr.close()
            self.client.ssh.close()
            print(f"[FileSystemsExecutor.close_c] SSH connection closed successfully.")
        except Exception as e:
            print(f"[FileSystemsExecutor.close_c] Error closing SSH connection: {e}")
        return

    ##################################################

    def parse_ls_r_output(self, output, max_depth=3):
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
        except Exception as e:
            print(f"[FileSystemsExecutor.parse_ls_r_output] Error parsing the output: {e}")
            return {}
        print(f"[FileSystemsExecutor.parse_ls_r_output] Parsed the SSH output successfully.")
        return root

    def retrieve_file_tree_schema(self):
        client = self.connect_c()
        try:
            query = INTERNAL_COMMAND_SETS[LIST_DIRECTORY_RECURSIVE][self.connection.os_type]
            stdin, stdout, stderr = client.exec_command(query)
            file_directory_tree = stdout.read().decode()
            print(f"[FileSystemsExecutor.retrieve_file_tree_schema] Retrieved the file tree schema successfully.")
            # convert directory tree to json
            directory_dict = json.dumps(self.parse_ls_r_output(file_directory_tree), default=str)
            directory_dict = directory_dict[:int(self.connection.os_read_limit_tokens)] if (
                len(directory_dict) > int(self.connection.os_read_limit_tokens)) else directory_dict
            print(f"[FileSystemsExecutor.retrieve_file_tree_schema] Directory dict is parsed successfully.")
        except Exception as e:
            print(f"[FileSystemsExecutor.retrieve_file_tree_schema] Error retrieving the file tree schema: {e}")
            directory_dict = "{}"
        self.close_c()
        print(f"[FileSystemsExecutor.retrieve_file_tree_schema] Closed the SSH connection successfully.")
        return directory_dict

    def execute_file_system_command_set(self, commands: list[str]):
        from apps._services.llms.utils import GPT_DEFAULT_ENCODING_ENGINE
        from apps._services.llms.utils import ChatRoles
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
            except Exception as e:
                results["status"] = False
                results["stdins"].append(command)
                results["stdouts"].append(f"Error executing the command: {str(e)}")
                results["stderrs"].append("")

        try:
            updated_schema = self.retrieve_file_tree_schema()
            print(f"[FileSystemsExecutor.execute_file_system_command_set] Updated the file tree schema successfully.")
            results["updated_schema"] = updated_schema
            self.close_c()
        except Exception as e:
            print(f"[FileSystemsExecutor.execute_file_system_command_set] Error closing the connection: {e}")

        try:
            transaction = LLMTransaction(
                organization=self.connection.assistant.organization,
                model=self.connection.assistant.llm_model,
                responsible_user=None,
                responsible_assistant=self.connection.assistant,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                llm_cost=ToolCostsMap.FileSystemsExecutor.COST,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=TransactionSourcesNames.FILE_SYSTEM_COMMANDS,
                is_tool_cost=True
            )
            transaction.save()
            print(f"[FileSystemsExecutor.execute_file_system_command_set] Saved the transaction successfully.")
        except Exception as e:
            print(f"[FileSystemsExecutor.execute_file_system_command_set] Error saving the transaction: {str(e)}")
        return results
