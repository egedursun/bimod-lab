#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_execute_auto_tasks.py
#  Last Modified: 2024-11-16 16:46:36
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-16 16:46:36
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

from celery import shared_task
from django.utils import timezone

from apps.core.tool_calls.utils import (
    VoidForgerModesNames
)

from apps.core.voidforger.voidforger_executor import (
    VoidForgerExecutionManager
)

from apps.voidforger.utils import (
    VoidForgerRuntimeStatusesNames
)

logger = logging.getLogger(__name__)


@shared_task
def execute_voidforgers_auto_cycle():
    from apps.voidforger.models import (
        VoidForger
    )

    voidforger_instances = VoidForger.objects.filter(
        runtime_status=VoidForgerRuntimeStatusesNames.ACTIVE
    )

    logger.info(f"VoidForger auto cycle execution started for {len(voidforger_instances)} VoidForgers.")  ###

    current_time = timezone.now()

    for voidforger_instance in voidforger_instances:

        last_auto_execution_time = voidforger_instance.last_auto_execution_ended_at
        interval_execution_minutes = voidforger_instance.auto_run_trigger_interval_minutes

        time_difference_minutes = None
        if last_auto_execution_time is not None:
            time_difference_minutes = (current_time - last_auto_execution_time).total_seconds() / 60

        logger.info(f"Time difference in minutes: {time_difference_minutes}")

        if time_difference_minutes is None or (time_difference_minutes >= interval_execution_minutes):
            logger.info(f"Dispatching subtask for VoidForger with ID: {voidforger_instance.id}.")

            execute_single_voidforger_cycle.delay(
                voidforger_instance.id
            )

    return True


@shared_task
def execute_single_voidforger_cycle(voidforger_id):
    from apps.voidforger.models import VoidForger

    try:
        voidforger_instance = VoidForger.objects.get(
            id=voidforger_id
        )

        xc = VoidForgerExecutionManager(
            user=voidforger_instance.user,
            voidforger_id=voidforger_instance.id
        )

        error = xc.run_cycle(
            trigger=VoidForgerModesNames.AUTOMATED
        )

        if error:
            logger.error(f"Error occurred while executing auto cycle for VoidForger with ID {voidforger_id}.")

            return False

    except Exception as e:
        logger.error(f"Error occurred while executing auto cycle for VoidForger with ID {voidforger_id}.")
        logger.error(e)

        return False
