#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_scheduled_job_logs_query.py
#  Last Modified: 2024-11-13 23:07:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 23:07:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json
import logging

from apps.assistants.models import Assistant

from apps.mm_scheduled_jobs.models import (
    ScheduledJobInstance
)

logger = logging.getLogger(__name__)


def run_query_execute_scheduled_job_logs(assistant: Assistant):
    try:
        job_execution_logs = ScheduledJobInstance.objects.filter(
            scheduled_job__assistant=assistant
        ).order_by(
            '-started_at'
        )[0:5]

        formatted_result = []

        for log in job_execution_logs:
            log: ScheduledJobInstance

            formatted_result.append(
                {
                    'status': log.status,
                    'logs': log.logs,
                    'execution_index': log.execution_index,
                    'started_at': log.started_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'ended_at': log.ended_at.strftime('%Y-%m-%d %H:%M:%S') if log.ended_at else "N/A",
                }
            )

        output = json.dumps(formatted_result)

    except Exception as e:
        logger.error(f"Error occurred while running the Scheduled Job Logs query: {e}")
        error = f"There has been an unexpected error on running the Scheduled Job Logs query: {e}"

        return error

    return output
