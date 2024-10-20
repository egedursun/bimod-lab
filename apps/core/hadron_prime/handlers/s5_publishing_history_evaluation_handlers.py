#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s5_publishing_history_evaluation_handlers.py
#  Last Modified: 2024-10-17 22:35:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:35:32
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

from apps.hadron_prime.models import HadronNode, HadronTopicMessage

logger = logging.getLogger(__name__)


def retrieve_publish_history_logs(node: HadronNode):
    publish_history_logs, error = "N/A", None

    memory_size = node.publishing_history_lookback_memory_size
    publish_history_log_objects = node.publishing_history_logs.all().order_by('-created_at')[:memory_size]

    logger.info("Retrieving publishing history logs.")
    publish_history_string = "[TOPIC_NAME | TOPIC_CATEGORY | MESSAGE | CREATED_AT]\n"
    for publish_history_log in publish_history_log_objects:
        publish_history_log: HadronTopicMessage
        publish_history_string += f"[{publish_history_log.topic.topic_name} | {publish_history_log.topic.topic_category} | {publish_history_log.message} | {publish_history_log.created_at}]\n"
    logger.info("Publishing history logs have been retrieved.")

    publish_history_logs = f"""
            ### **NODE TOPIC SELF-PUBLISHING HISTORY LOGS:**
            '''
            {publish_history_string}
            '''
        """
    logger.info("Publishing history logs have been embedded.")
    return publish_history_logs, error
