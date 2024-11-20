#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_012_drafting_folder_create.py
#  Last Modified: 2024-11-18 22:24:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 22:30:27
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

from apps.drafting.models import DraftingFolder
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__012_drafting_folder_create(
    metadata__user,
    metadata__organization
):
    try:
        new_drafting_folder = DraftingFolder.objects.create(
            organization=metadata__organization,
            created_by_user=metadata__user,
            name=f"Generic Drafting Folder for {metadata__organization.name} {generate_random_object_id_string()}",
            description=f"This is a generic drafting folder for primary drafting operations of organization {metadata__organization.name}.",
            meta_context_instructions=f"This is a generic drafting folder for primary drafting operations of organization {metadata__organization.name}."
        )

    except Exception as e:
        logger.error(f"Error in action__012_drafting_folder_create: {e}")
        return False, None

    logger.info(f"New drafting folder created successfully: {new_drafting_folder}")
    return True, new_drafting_folder
