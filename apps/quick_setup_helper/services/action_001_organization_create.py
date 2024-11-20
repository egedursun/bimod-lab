#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_001_organization_create.py
#  Last Modified: 2024-11-18 20:37:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-18 20:37:26
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

from apps.organization.models import Organization
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__001_organization_create(
    metadata__user,
    response__organization_name,
    response__organization_description
):
    try:
        # Create the organization
        new_organization = Organization.objects.create(
            name=response__organization_name + " " + generate_random_object_id_string(),
            description=response__organization_description,
            created_by_user=metadata__user,
            last_updated_by_user=metadata__user
        )
        new_organization.users.set([metadata__user])
        new_organization.save()

    except Exception as e:
        logger.error(f"Error in action__001_organization_create: {e}")
        return False, None

    logger.info("action__001_organization_create completed successfully.")
    return True, new_organization
