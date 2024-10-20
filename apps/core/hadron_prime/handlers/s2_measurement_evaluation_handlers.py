#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: measurement_handlers.py
#  Last Modified: 2024-10-17 22:29:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:29:10
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

from apps.core.hadron_prime.parsers import make_request_from_curl
from apps.hadron_prime.models import HadronNode


logger = logging.getLogger(__name__)


def evaluate_measurements(node: HadronNode):
    measurement_data, error = "N/A", None
    measurement_curl = node.measurements_curl
    try:
        response_text = make_request_from_curl(curl_command=measurement_curl)
    except Exception as e:
        logger.error(f"Error occurred while evaluating measurements: {str(e)}")
        error = str(e)
        return measurement_data, error
    if not response_text:
        logger.error("State data could not have been received.")
        error = "State data could not have been received."
        return measurement_data, error

    measurement_data = f"""
        ### **SENSORY MEASUREMENTS:**
        '''
        {response_text}
        '''

        -----
    """
    logger.info("Measurement data has been evaluated.")
    return measurement_data, error
