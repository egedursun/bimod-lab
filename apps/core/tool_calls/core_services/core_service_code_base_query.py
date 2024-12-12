#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_code_base_query.py
#  Last Modified: 2024-10-05 02:26:00
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

from apps.core.codebase.codebase_executor import (
    CodeRepositoryExecutor
)

logger = logging.getLogger(__name__)


def run_query_code_base(
    c_id: int,
    repository_uri: str,
    query_content_str: str,
):
    try:
        cli = CodeRepositoryExecutor(
            connection_id=c_id
        )

        output = cli.search_within_code_chunks(
            repository_uri=repository_uri,
            query=query_content_str,
        )

        logger.info(f"Code base query output: {output}")

    except Exception as e:
        logger.error(f"Error occurred while running the codebase query: {e}")
        error = f"There has been an unexpected error on running the codebase query: {e}"

        return error

    return output
