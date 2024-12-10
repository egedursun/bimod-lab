#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s9_analytical_calculation_handlers.py
#  Last Modified: 2024-10-17 22:39:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:39:10
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


def calculate_analytical_data(node: HadronNode):
    analytical_data, error = "N/A", None
    analytical_data_curl = node.analytic_calculation_curl

    try:
        response_text = make_request_from_curl(
            curl_command=analytical_data_curl
        )

    except Exception as e:
        logger.error(f"Error occurred while evaluating analytical data: {str(e)}")
        error = str(e)

        return analytical_data, error

    if not response_text:
        logger.error("Analytical data could not have been received.")
        error = "Analytical data could not have been received."

        return analytical_data, error

    analytical_data = f"""
        ### **DETERMINISTIC ANALYTICAL CALCULATION RESULTS:**
        '''
        {response_text}
        '''

        -----
    """

    logger.info("Analytical data has been evaluated.")

    return analytical_data, error
