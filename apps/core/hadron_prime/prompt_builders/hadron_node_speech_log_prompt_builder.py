#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_node_speech_log_prompt_builder.py
#  Last Modified: 2024-10-22 14:14:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 14:14:05
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

from apps.core.hadron_prime.handlers import structure_topic_messages, retrieve_publish_history_logs, \
    retrieve_sease_logs
from apps.core.hadron_prime.prompts import build_optional_instructions_prompt, build_system_metadata_prompt, \
    build_node_metadata_prompt
from apps.core.hadron_prime.prompts.hadron_node_speech_generation_instructions_prompt import \
    hadron_node_speech_generation_core_instructions_prompt, hadron_node_speech_logs_prompt, \
    hadron_node_execution_logs_prompt
from apps.hadron_prime.models import HadronNode


logger = logging.getLogger(__name__)


def build_hadron_node_speech_log_prompt(node: HadronNode):
    merged_instructions = ""
    merged_instructions += hadron_node_speech_generation_core_instructions_prompt()
    merged_instructions += build_optional_instructions_prompt(node=node)
    merged_instructions += build_system_metadata_prompt(node=node)
    merged_instructions += build_node_metadata_prompt(node=node)

    messages_for_topic, error = structure_topic_messages(node=node)
    if error:
        logger.error(f"Error while structuring topic messages for node, skipping...")
    else:
        merged_instructions += messages_for_topic

    self_publishes_for_topics, error = retrieve_publish_history_logs(node=node)
    if error:
        logger.error(f"Error while retrieving publish history logs for node, skipping...")
    else:
        merged_instructions += self_publishes_for_topics

    logs_for_sease, error = retrieve_sease_logs(node=node)
    if error:
        logger.error(f"Error while retrieving SEASE logs for node, skipping...")
    else:
        merged_instructions += logs_for_sease

    logs_for_speech, error = hadron_node_speech_logs_prompt(node=node)
    if error:
        logger.error(f"Error while retrieving speech logs for node, skipping...")
    else:
        merged_instructions += logs_for_speech

    logs_for_execution, error = hadron_node_execution_logs_prompt(node=node)
    if error:
        logger.error(f"Error while retrieving execution logs for node, skipping...")
    else:
        merged_instructions += logs_for_execution

    return merged_instructions
