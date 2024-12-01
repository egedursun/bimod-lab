#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_ssh_system_command.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
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

from apps.core.file_systems.file_systems_executor import FileSystemsExecutor
from apps.datasource_file_systems.models import DataSourceFileSystem


logger = logging.getLogger(__name__)


def run_execute_ssh_system_commands(
    c_id: int,
    bash_commands: list[str]
):

    conn = DataSourceFileSystem.objects.get(
        id=c_id
    )

    try:
        cli = FileSystemsExecutor(
            connection=conn
        )

        output = cli.execute_file_system_command_set(
            commands=bash_commands
        )

        logger.info(f"File system command execution output: {output}")

    except Exception as e:
        logger.error(f"Error occurred while executing the file system commands: {e}")
        error_msg = f"Error occurred while executing the file system commands: {str(e)}"
        return error_msg

    return output
