#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_014_sheetos_folder_create.py
#  Last Modified: 2024-11-18 22:25:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:25:06
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

from apps.quick_setup_helper.utils import generate_random_object_id_string
from apps.sheetos.models import SheetosFolder


logger = logging.getLogger(__name__)


def action__014_sheetos_folder_create(
    metadata__user,
    metadata__organization
):
    try:
        new_sheetos_folder = SheetosFolder.objects.create(
            organization=metadata__organization,
            created_by_user=metadata__user,
            name=f"Generic Sheetos Folder for {metadata__organization.name} {generate_random_object_id_string()}",
            description=f"This is a generic sheetos management folder for primary spreadsheet operations of organization {metadata__organization.name}.",
            meta_context_instructions=f"This is a generic sheetos management folder for primary spreadsheet operations of organization {metadata__organization.name}."
        )

    except Exception as e:
        logger.error(f"Error in action__014_sheetos_folder_create: {e}")
        return False, None

    logger.info(f"New sheetos folder created successfully: {new_sheetos_folder}")
    return True, new_sheetos_folder
