#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s10_perform_actuation_handlers.py
#  Last Modified: 2024-10-17 22:38:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:38:40
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

from apps.core.hadron_prime.parsers import parse_curl

from apps.hadron_prime.models import HadronNode
import json

logger = logging.getLogger(__name__)


def perform_actuation(node: HadronNode, determined_action: str):
    success, error = True, None
    actuation_data_curl = node.actuation_curl
    determined_action_json = json.loads(determined_action)

    try:
        method, url, headers, data = parse_curl(
            curl_command=actuation_data_curl
        )

        data = determined_action_json

        import requests
        response = requests.request(
            method,
            url,
            headers=headers,
            data=json.dumps(data)
        )

        response_status = response.status_code

        if str(response_status).startswith("2"):

            return success, error

        else:
            error = f"Actuation failed with status code: {response_status}"

            return False, error

    except Exception as e:
        logger.error(f"Error occurred while triggering actuation: {str(e)}")
        error = str(e)

        return False, error

    if not response_text:
        logger.error("Actuation could not have been triggered.")
        error = "Actuation could not have been triggered."

        return False, error

    logger.info("Actuation has been triggered successfully.")

    return success, error
