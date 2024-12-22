#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-28 19:37:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:37:03
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

import boto3
import filetype

from apps.core.code_analyst.utils import (
    BIN_FILE_FORMAT
)

from apps.export_assistants.utils import (
    generate_save_name
)

from config import settings
from config.settings import MEDIA_URL

logger = logging.getLogger(__name__)


def save_image_and_provide_full_uri(image_bytes):
    from apps.core.metatempo.utils import (
        METATEMPO_IMAGES_ROOT_MEDIA_PATH
    )

    guess_file_type = filetype.guess(image_bytes)

    if guess_file_type is None:
        guess_file_type = BIN_FILE_FORMAT

    extension = guess_file_type.extension

    save_name = generate_save_name(
        extension=extension
    )

    s3_path = f"{METATEMPO_IMAGES_ROOT_MEDIA_PATH}{save_name}"
    full_uri = f"{MEDIA_URL}{s3_path}"

    try:
        s3c = boto3.client('s3')
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        s3c.put_object(
            Bucket=bucket,
            Key=s3_path,
            Body=image_bytes
        )

        logger.info(f"[save_image_and_provide_full_uri] Image saved to S3 with URI: {full_uri}")

    except Exception as e:
        logger.error(f"[save_image_and_provide_full_uri] Error occurred while saving the image to S3: {e}")

        return None

    return full_uri


def find_tool_call_from_json_single(response: str):
    logger.info("Finding [SINGLE] tool call from JSON response.")

    response = (
        response.replace('```json', '')
        .replace('```', '')
        .replace('`', '')
    )

    json_objects = []

    if response is None or response == "":
        return json_objects

    if "{" and "}" not in response:
        return json_objects

    c = response[0]

    while c != "{":
        response = response[1:]
        c = response[0]

    cb = response[-1]

    while cb != "}":
        response = response[:-1]
        cb = response[-1]

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

    if len(json_objects) > 0:
        return json_objects[0]

    return json_objects
