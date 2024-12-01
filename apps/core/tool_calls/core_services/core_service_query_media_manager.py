#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_query_media_manager.py
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

from apps.core.media_managers.media_manager_execution_handler import MediaManager
from apps.core.tool_calls.utils import AnalysisToolCallExecutionTypesNames
from apps.datasource_media_storages.models import DataSourceMediaStorageConnection
from apps.multimodal_chat.models import MultimodalChat


logger = logging.getLogger(__name__)


def run_query_media_manager(
    c_id,
    chat_id,
    manager_file_type,
    f_uris,
    manager_query,
    no_chat=False
):

    conn = DataSourceMediaStorageConnection.objects.get(
        id=c_id
    )

    chat = None
    if no_chat is False:
        chat = MultimodalChat.objects.get(
            id=chat_id
        )

    try:
        xc = MediaManager(
            connection=conn,
            chat=chat
        )

        output, f_uris, img_uris = "", [], []

        if manager_file_type == AnalysisToolCallExecutionTypesNames.FILE_INTERPRETATION:

            logger.info(f"Executing the storage query: {manager_query}")
            output = xc.interpretation_handler_method(
                full_file_paths=f_uris,
                query_string=manager_query
            )

            f_uris = output.get("file_uris")
            img_uris = output.get("image_uris")

        elif manager_file_type == AnalysisToolCallExecutionTypesNames.IMAGE_INTERPRETATION:

            logger.info(f"Executing the storage query: {manager_query}")
            output = xc.interpretation_image_handler_method(
                full_image_paths=f_uris,
                query_string=manager_query
            )

    except Exception as e:
        logger.error(f"Error occurred while executing the storage query: {e}")
        error = f"Error occurred while executing the storage query: {str(e)}"
        return error, [], []

    logger.info(f"Storage query output: {output}")
    return output, f_uris, img_uris
