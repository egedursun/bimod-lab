#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_repository_upload_log_tasks.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
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


def add_repository_upload_log(document_full_uri, log_name):
    from apps.datasource_codebase.models import RepositoryProcessingLog
    RepositoryProcessingLog.objects.create(
        repository_full_uri=document_full_uri,
        log_message=log_name
    )
    logger.info(f"Repository Upload Log Created: {document_full_uri} - {log_name}")
    return
