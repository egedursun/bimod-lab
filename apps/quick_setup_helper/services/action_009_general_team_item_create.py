#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_009_general_team_item_create.py
#  Last Modified: 2024-11-18 22:24:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:24:10
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

from apps.projects.models import (
    ProjectTeamItem
)

from apps.quick_setup_helper.utils import (
    generate_random_object_id_string
)

logger = logging.getLogger(__name__)


def action__009_general_team_item_create(
    metadata__user,
    metadata__project_item
):
    try:

        new_team_item = ProjectTeamItem.objects.create(
            project=metadata__project_item,
            team_lead=metadata__user,
            created_by_user=metadata__user,
            team_name=f"Core Team for Project {metadata__project_item.project_name} {generate_random_object_id_string()}",
            team_description=f"The core management team created for generic operations within project {metadata__project_item.project_name}.",
        )

        new_team_item.team_members.set(
            [
                metadata__user
            ]
        )

        new_team_item.save()

    except Exception as e:
        logger.error(f"Error in action__009_general_team_item_create: {e}")

        return False, None

    logger.info(f"New team item created successfully: {new_team_item}")

    return True, new_team_item
