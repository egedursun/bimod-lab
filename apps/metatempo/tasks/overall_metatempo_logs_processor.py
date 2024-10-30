#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: overall_metatempo_logs_processor.py
#  Last Modified: 2024-10-29 22:46:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 22:46:42
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
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from apps.core.generative_ai.utils import GPT_DEFAULT_ENCODING_ENGINE, ChatRoles
from apps.core.internal_cost_manager.costs_map import InternalServiceCosts
from apps.core.metatempo.metatempo_execution_handler import MetaTempoExecutionManager
from apps.llm_transaction.models import LLMTransaction
from apps.llm_transaction.utils import LLMTransactionSourcesTypesNames
from apps.metakanban.models import MetaKanbanBoard
from apps.metatempo.models import MetaTempoConnection, MetaTempoProjectOverallLog
from apps.metatempo.utils import MetaTempoOverallLogIntervalsNames
from apps.projects.models import ProjectItem, ProjectTeamItem

logger = logging.getLogger(__name__)


@shared_task
def generate_period_overall_metatempo_logs():
    # Retrieve all connections
    connections = MetaTempoConnection.objects.filter(is_tracking_active=True, )
    if not connections:
        return True

    try:
        # Process overall logs
        for connection in connections:

            last_tracked_log = MetaTempoProjectOverallLog.objects.filter(metatempo_connection=connection)
            if not last_tracked_log:
                last_tracked_log = None
            else:
                last_tracked_log = last_tracked_log.order_by('-created_at').first()

            delta_value_hours = 0
            recording_interval = connection.overall_log_intervals
            if recording_interval == MetaTempoOverallLogIntervalsNames.DAILY:
                delta_value_hours = 24 * 1
            elif recording_interval == MetaTempoOverallLogIntervalsNames.BI_DAILY:
                delta_value_hours = 24 * 2
            elif recording_interval == MetaTempoOverallLogIntervalsNames.WEEKLY:
                delta_value_hours = 24 * 7
            elif recording_interval == MetaTempoOverallLogIntervalsNames.BI_WEEKLY:
                delta_value_hours = 24 * 14
            elif recording_interval == MetaTempoOverallLogIntervalsNames.MONTHLY:
                delta_value_hours = 24 * 30

            if last_tracked_log:
                time_since_last_log_creation = (timezone.now() - last_tracked_log.created_at)
                if time_since_last_log_creation > timedelta(hours=delta_value_hours):
                    # Create a new log as the last log is older than the interval
                    print(
                        f"Creating a new log as the last log is older than the interval for connection {connection.id}")
                    pass
                else:
                    print(f"Must not create a new log as the last log is not older than the interval for "
                          f"connection {connection.id}, skipping...")
                    # There is no need to create a new log as the last log is not older than the interval
                    logger.info(f"Must not create a new log as the last log is not older than the interval for "
                                f"connection {connection.id}, skipping...")
                    continue
            else:
                # Create a new log as there is no log yet
                print(f"Creating a new log as there is no log yet for connection {connection.id}")
                pass
            try:
                xc = (MetaTempoExecutionManager(metatempo_connection_id=connection.id))
                _, error = xc.interpret_overall_logs()
                if error:
                    logger.error(f"Error while processing the overall logs for connection {connection.id}: {error}")
                    continue

            except Exception as e:
                logger.error(f"Error while processing the overall logs for connection {connection.id}: {e}")
                continue

            try:
                tx = LLMTransaction(
                    organization=connection.board.project.organization, model=connection.board.llm_model,
                    responsible_user=connection.board.created_by_user, responsible_assistant=None,
                    encoding_engine=GPT_DEFAULT_ENCODING_ENGINE, llm_cost=InternalServiceCosts.MetaTempo.COST,
                    transaction_type=ChatRoles.SYSTEM,
                    transaction_source=LLMTransactionSourcesTypesNames.METATEMPO, is_tool_cost=True
                )
                tx.save()
                logger.info(f"[interpret_overall_logs] Created LLMTransaction for MetaTempo [AUTO] Overall Analysis Log.")
            except Exception as e:
                logger.error(
                    f"[interpret_overall_logs] Error creating LLMTransaction for MetaTempo [AUTO] Overall Analysis Log. Error: {e}")
                pass

    except Exception as e:
        logger.error(f"Error while processing the overall logs: {e}")
        return False

    logger.info(f"Successfully processed the overall logs.")
    return True
