#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_file_system_schema_search.py
#  Last Modified: 2024-12-04 01:31:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-04 01:31:53
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

logger = logging.getLogger(__name__)


def run_query_search_file_system_directory_schema(
    connection_id: str,
    query: str
):
    from apps.core.file_systems.file_systems_executor import (
        FileSystemsExecutor
    )
    from apps.datasource_file_systems.models import (
        DataSourceFileSystem
    )

    try:
        connection = DataSourceFileSystem.objects.get(id=connection_id)
        if not connection:
            return f"Connection with ID: {connection_id} does not exist."

        xc = FileSystemsExecutor(
            connection=connection
        )

        output = xc.search_file_system_directory_schema(
            query=query
        )

    except Exception as e:
        logger.error(f"Error occurred while executing the SSH File System Directory Schema Search query: {str(e)}")
        error_msg = f"Error occurred while executing the SSH File System Directory Schema Search query: {str(e)}"
        return error_msg

    return output
