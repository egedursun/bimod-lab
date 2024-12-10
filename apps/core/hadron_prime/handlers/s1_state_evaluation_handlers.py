#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s1_state_evaluation_handlers.py
#  Last Modified: 2024-10-17 22:29:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:29:53
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

from apps.core.hadron_prime.parsers import (
    make_request_from_curl
)

from apps.hadron_prime.models import HadronNode


logger = logging.getLogger(__name__)


def evaluate_state(node: HadronNode):
    current_state_data, goal_state_data, error = "N/A", "N/A", None

    current_state_curl = node.current_state_curl
    try:
        response_text_current = make_request_from_curl(
            curl_command=current_state_curl
        )

    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while evaluating state: {e}")

        return current_state_data, goal_state_data, error

    if not response_text_current:
        logger.error("Current state data could not have been received.")
        error = "Current state data could not have been received."

        return current_state_data, goal_state_data, error

    current_state_data = f"""
        ### **CURRENT STATE:**
        '''
        {response_text_current}
        '''

        -----
    """
    logger.info("Current state data has been evaluated.")

    goal_state_curl = node.goal_state_curl

    try:
        response_text_goal = make_request_from_curl(
            curl_command=goal_state_curl
        )

    except Exception as e:
        error = str(e)
        logger.error(f"Error occurred while evaluating goal state: {error}")

        return current_state_data, goal_state_data, error

    if not response_text_goal:
        logger.error("Goal state data could not have been received.")
        error = "Goal state data could not have been received."

        return current_state_data, goal_state_data, error

    goal_state_data = f"""
        ### **GOAL STATE:**
        '''
        {response_text_goal}
        '''
    """

    logger.info("Goal state data has been evaluated.")

    return current_state_data, goal_state_data, error
