#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_008_general_project_item_create.py
#  Last Modified: 2024-11-18 22:21:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:21:45
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

from apps.assistants.models import Assistant
from apps.projects.models import ProjectItem
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__008_general_project_item_create(
    metadata__user,
    metadata__organization,
    metadata__assistants
):
    try:

        # Create the project item
        new_project_item = ProjectItem.objects.create(
            organization=metadata__organization,
            project_name=f"General Project for Organization {metadata__organization.name} {generate_random_object_id_string()}",
            project_department=f"General Department {generate_random_object_id_string()}",
            project_description=f"The main wrapper project for organization {metadata__organization.name} created for generic operations.",
            created_by_user=metadata__user,
        )

        # Connect the project to assistants
        try:
            for assistant in metadata__assistants:
                assistant: Assistant

                assistant.project_items.add(new_project_item) if assistant.project_items else assistant.project_items.set([new_project_item])
                assistant.save()

        except Exception as e:
            logger.error(f"Error while connecting assistants to the new project item: {e}")
            return False, None

    except Exception as e:
        logger.error(f"Error in action__008_general_project_item_create: {e}")
        return False, None

    logger.info(f"New project item created successfully: {new_project_item}")
    return True, new_project_item
