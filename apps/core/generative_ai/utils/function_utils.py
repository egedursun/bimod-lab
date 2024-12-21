#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 02:20:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
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
import re
import uuid
from json import JSONDecoder

import apps.core

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


def extract_image_uri(
    response_str
):
    logger.info("Extracting image URI from response.")
    pattern = r'"image_uri":\s*"([^"]+)"'
    match = re.search(pattern, response_str)

    return match.group(1) if match else None


def extract_file_uri(
    response_str
):
    logger.info("Extracting file URI from response.")
    pattern = r'"file_uri":\s*"([^"]+)"'
    match = re.search(pattern, response_str)

    return match.group(1) if match else None


def generate_random_audio_filename(
    extension="mp3"
):
    uuid1 = str(uuid.uuid4())
    uuid2 = str(uuid.uuid4())
    filename = f"generated_audio_{uuid1}_{uuid2}.{extension}"

    return filename


def step_back_retry_mechanism(
    client,
    latest_message,
    caller="respond"
):
    logger.info("Step back retry mechanism.")

    from apps.core.generative_ai.utils import (
        RetryCallersNames,
        DEFAULT_ERROR_MESSAGE
    )

    if apps.core.generative_ai.utils.constant_utils.ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:

        apps.core.generative_ai.utils.constant_utils.ACTIVE_RETRY_COUNT += 1

        if caller == RetryCallersNames.RESPOND:
            return client.respond_stream(
                latest_message=latest_message
            )

        elif caller == RetryCallersNames.RESPOND_STREAM:
            return client.respond_stream(
                latest_message=latest_message
            )

        else:
            return DEFAULT_ERROR_MESSAGE

    else:
        return DEFAULT_ERROR_MESSAGE
