#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s4_sease_history_evaluation_handlers.py
#  Last Modified: 2024-10-17 22:35:18
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:35:19
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

from apps.hadron_prime.models import HadronNode, HadronStateErrorActionStateErrorLog


logger = logging.getLogger(__name__)


def retrieve_sease_logs(node: HadronNode):
    sease_logs, error = "N/A", None
    memory_size = node.state_action_state_lookback_memory_size
    sease_log_objects = node.state_action_state_history_logs.all().order_by('-created_at')[:memory_size]

    logger.info("Retrieving SEASE logs.")
    sease_logs_string = "[OLD_STATE & OLD_ERROR] -> [ACTION] -> [NEW_STATE & NEW_ERROR]\n"

    for sease_log in sease_log_objects:
        sease_log: HadronStateErrorActionStateErrorLog
        sease_logs_string += f"[S(t-1): {sease_log.old_state} & E(t-1): {sease_log.old_error}] -> [A(t): {sease_log.action}] -> [S(t): {sease_log.new_state} & E(t): {sease_log.new_error}]\n"
    logger.info("SEASE logs have been retrieved.")

    sease_logs = f"""
        ### **STATE-ERROR-ACTION-STATE-ERROR LOGS:**
        '''
        {sease_logs_string}
        '''
    """
    logger.info("SEASE logs have been embedded.")
    return sease_logs, error
