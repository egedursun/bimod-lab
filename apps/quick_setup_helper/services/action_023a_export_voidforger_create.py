#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_023a_export_voidforger_create.py
#  Last Modified: 2024-12-09 16:39:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-09 16:39:20
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

from django.contrib.auth.models import User

from apps.export_voidforger.models import (
    ExportVoidForgerAPI
)

from apps.llm_core.models import LLMCore
from apps.organization.models import Organization
from apps.voidforger.models import VoidForger

logger = logging.getLogger(__name__)


def action__023a_export_voidforger_create(
    metadata__user,
    metadata__organization,
    metadata__llm_model
):
    metadata__user: User
    metadata__organization: Organization
    metadata__llm_model: LLMCore

    try:

        voidforger_object, created = VoidForger.objects.get_or_create(
            user=metadata__user
        )

        if voidforger_object.llm_model is None:
            voidforger_object.llm_model = metadata__llm_model
            voidforger_object.save()

        # Create the exportation of the VoidForger object.

        voidforger_api = ExportVoidForgerAPI.objects.create(
            organization=metadata__organization,
            voidforger=voidforger_object,
            created_by_user=metadata__user
        )

        voidforger_api.save()

    except Exception as e:
        logger.error(f"Error while creating/exporting VoidForger object: {e}")

        return False

    logger.info("action__023a_export_voidforger_create completed successfully.")

    return True
