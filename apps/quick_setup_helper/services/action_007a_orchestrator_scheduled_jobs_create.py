#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: action_007a_scheduled_jobs_create.py
#  Last Modified: 2024-11-20 15:08:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-20 15:08:24
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

from apps.mm_scheduled_jobs.models import OrchestrationScheduledJob
from apps.orchestrations.models import Maestro
from apps.quick_setup_helper.utils import generate_random_object_id_string

logger = logging.getLogger(__name__)


def action__007a_orchestrator_scheduled_jobs_create(
    metadata__user,
    metadata__orchestrators,
    response__scheduled_job_interval,
    response__scheduled_job_description,
    response__scheduled_job_step_guides
):

    if response__scheduled_job_interval == "per_minute":
        interval_specifier_minute = "*"
        interval_specifier_hour = "*"
        interval_specifier_day_of_week = "*"
        interval_specifier_day_of_month = "*"
        interval_specifier_month_of_year = "*"
    elif response__scheduled_job_interval == "per_hour":
        interval_specifier_minute = "0"
        interval_specifier_hour = "*"
        interval_specifier_day_of_week = "*"
        interval_specifier_day_of_month = "*"
        interval_specifier_month_of_year = "*"
    elif response__scheduled_job_interval == "per_day":
        interval_specifier_minute = "0"
        interval_specifier_hour = "0"
        interval_specifier_day_of_week = "*"
        interval_specifier_day_of_month = "*"
        interval_specifier_month_of_year = "*"
    elif response__scheduled_job_interval == "per_week":
        interval_specifier_minute = "0"
        interval_specifier_hour = "0"
        interval_specifier_day_of_week = "1"
        interval_specifier_day_of_month = "*"
        interval_specifier_month_of_year = "*"
    elif response__scheduled_job_interval == "per_month":
        interval_specifier_minute = "0"
        interval_specifier_hour = "0"
        interval_specifier_day_of_week = "*"
        interval_specifier_day_of_month = "1"
        interval_specifier_month_of_year = "*"
    elif response__scheduled_job_interval == "per_year":
        interval_specifier_minute = "0"
        interval_specifier_hour = "0"
        interval_specifier_day_of_week = "*"
        interval_specifier_day_of_month = "1"
        interval_specifier_month_of_year = "1"
    else:
        logger.error(f"Invalid interval specifier: {response__scheduled_job_interval}")
        return False

    try:
        for orchestrator in metadata__orchestrators:
            orchestrator: Maestro

            try:

                OrchestrationScheduledJob.objects.create(
                    maestro=orchestrator,
                    name=f"Automated Scheduled Job for Orchestration Maestro {orchestrator.name} {generate_random_object_id_string()}",
                    task_description=response__scheduled_job_description,
                    step_guide=response__scheduled_job_step_guides,
                    minute=interval_specifier_minute,
                    hour=interval_specifier_hour,
                    day_of_week=interval_specifier_day_of_week,
                    day_of_month=interval_specifier_day_of_month,
                    month_of_year=interval_specifier_month_of_year,
                    current_run_count=0,
                    maximum_runs=1000,
                    created_by_user=metadata__user
                )

            except Exception as e:
                logger.error(f"Failed to create scheduled job for orchestrator {orchestrator.name}: {str(e)}")
                continue

    except Exception as e:
        logger.error(f"Error in action__007a_orchestrator_scheduled_jobs_create: {str(e)}")
        return False

    logger.info("action__007a_orchestrator_scheduled_jobs_create completed successfully.")
    return True
