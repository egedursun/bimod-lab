#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s6_calculate_current_error_handlers.py
#  Last Modified: 2024-10-17 22:36:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:36:00
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


def calculate_error_data(node: HadronNode):
    error_calculation_data, error = "N/A", None
    error_measurement_curl = node.error_calculation_curl

    try:
        response_text = make_request_from_curl(
            curl_command=error_measurement_curl
        )

    except Exception as e:
        logger.error(f"Error occurred while evaluating error calculation: {str(e)}")
        error = str(e)

        return error_calculation_data, error

    if not response_text:
        logger.error("Error calculation data could not have been received.")
        error = "Error calculation data could not have been received."

        return error_calculation_data, error

    error_calculation_data = f"""
        ### **ERROR CALCULATION DATA:**
        '''
        {response_text}
        '''

        -----
    """

    logger.info("Error calculation data has been evaluated.")

    return error_calculation_data, error
