#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action__010_metakanban_board_create.py
#  Last Modified: 2024-11-18 22:24:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:24:19
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
import secrets

from apps.assistants.models import Assistant

from apps.metakanban.models import (
    MetaKanbanBoard,
    MetaKanbanAssistantConnection
)

from apps.metakanban.utils import (
    META_KANBAN_BOARD_API_KEY_DEFAULT_LENGTH
)

from apps.projects.models import ProjectItem

from apps.quick_setup_helper.utils import (
    generate_random_object_id_string
)

logger = logging.getLogger(__name__)


def action__010_metakanban_board_create(
    metadata__user,
    metadata__organization,
    metadata__llm_core,
    metadata__assistants,
    metadata__project: ProjectItem
):
    try:

        connection_api_key = secrets.token_urlsafe(
            META_KANBAN_BOARD_API_KEY_DEFAULT_LENGTH
        )

        new_metakanban_board = MetaKanbanBoard.objects.create(
            project=metadata__project,
            llm_model=metadata__llm_core,
            title=f"Meta Kanban Board for Project {metadata__project.project_name} {generate_random_object_id_string()}",
            description=f"The meta kanban board created for generic operations within project {metadata__project.project_name}.",
            created_by_user=metadata__user,
            connection_api_key=connection_api_key
        )

    except Exception as e:
        logger.error(f"Error in action__010_metakanban_board_create: {e}")

        return False, None

    # Connect MetaKanban board to Assistants

    try:
        for assistant in metadata__assistants:
            assistant: Assistant

            MetaKanbanAssistantConnection.objects.create(
                assistant=assistant,
                metakanban_board=new_metakanban_board,
                created_by_user=metadata__user
            )

    except Exception as e:
        logger.error(f"Error while connecting assistants to the new MetaKanban board: {e}")

        return False, None

    logger.info(f"New MetaKanban board created successfully: {new_metakanban_board}")

    return True, new_metakanban_board
