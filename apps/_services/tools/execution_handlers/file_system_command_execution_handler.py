#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: file_system_command_execution_handler.py
#  Last Modified: 2024-09-28 22:17:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:36:33
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
#  File: file_system_command_execution_handler.py
#  Last Modified: 2024-09-28 00:42:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:14:22
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from apps._services.file_systems.file_systems_executor import FileSystemsExecutor
from apps.datasource_file_systems.models import DataSourceFileSystem


def execute_file_system_commands(connection_id: int, commands: list[str]):
    file_system_connection = DataSourceFileSystem.objects.get(id=connection_id)
    print(
        f"[file_system_command_execution_handler.execute_file_system_commands] Executing file system commands: {commands}.")
    try:
        client = FileSystemsExecutor(connection=file_system_connection)
        file_system_response = client.execute_file_system_command_set(commands=commands)
    except Exception as e:
        error = (f"[file_system_command_execution_handler.execute_file_system_commands] Error occurred while "
                 f"executing the file system commands: {str(e)}")
        return error
    print(
        f"[file_system_command_execution_handler.execute_file_system_commands] File system commands executed "
        f"successfully.")
    return file_system_response
