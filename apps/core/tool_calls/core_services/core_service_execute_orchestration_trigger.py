#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_orchestration_trigger.py
#  Last Modified: 2024-11-13 05:09:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:10:58
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

from apps.core.orchestration.orchestration_executor import (
    OrchestrationExecutor
)

from apps.orchestrations.models import (
    OrchestrationReactantAssistantConnection,
    OrchestrationQuery,
    OrchestrationQueryLog
)

from apps.orchestrations.utils import (
    OrchestrationQueryLogTypesNames
)

logger = logging.getLogger(__name__)


def run_query_trigger_orchestration(
    user: User,
    c_id: int,
    user_query: str
):
    try:

        attached_images = []
        attached_files = []

        connection = OrchestrationReactantAssistantConnection.objects.get(
            id=c_id
        )

        query = OrchestrationQuery.objects.create(
            maestro=connection.orchestration_maestro,
            query_text=user_query,
            created_by_user=user,
            last_updated_by_user=user
        )

        query_text = query.query_text

        query_log = OrchestrationQueryLog.objects.create(
            orchestration_query=query,
            log_type=OrchestrationQueryLogTypesNames.USER,
            log_text_content=query_text + f"""
                                -----
                                **IMAGE URLS:**
                                '''
                                {attached_images}
                                '''
                                -----
                                **FILE URLS:**
                                '''
                                {attached_files}
                                '''
                                -----
                            """,
            log_file_contents=attached_files,
            log_image_contents=attached_images
        )

        query.logs.add(query_log)
        query.save()

        xc = OrchestrationExecutor(
            maestro=connection.orchestration_maestro,
            query_chat=query
        )

        output = xc.execute_for_query()

    except Exception as e:
        logger.error(f"Error occurred while running the Orchestration triggering execution tool: {e}")
        error = f"There has been an unexpected error on running the Orchestration triggering execution tool: {e}"

        return error

    return output
