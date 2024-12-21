#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-17 22:28:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:28:34
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import json
import logging

logger = logging.getLogger(__name__)


def find_tool_call_from_json(response: str):
    logger.info("Finding tool call from JSON response.")

    response = (
        response.replace('```json', '')
        .replace('```', '')
        .replace('`', '')
    )

    json_objects = []

    try:
        parsed_response = json.loads(response)

        if isinstance(parsed_response, list):
            for item in parsed_response:

                try:
                    json_object = json.loads(
                        item
                    )

                    json_objects.append(
                        json_object
                    )

                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to decode an item: {e}")
        else:
            json_objects.append(
                json.loads(
                    response
                )
            )

    except json.JSONDecodeError as e:
        logger.warning(f"Failed to parse response as JSON: {e}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    return json_objects
