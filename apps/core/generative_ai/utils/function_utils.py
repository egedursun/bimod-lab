#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
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
#   For permission inquiries, please contact: admin@br6.in.
#
#
#

import re
import uuid
from json import JSONDecoder

import apps.core


def find_tool_call_from_json(response: str, decoder=JSONDecoder()):
    response = f"""{response}"""
    response = response.replace("\n", "").replace("'", '"')
    json_objects = []
    pos = 0
    while True:
        match = response.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(response[match:])
            json_objects.append(result)
            pos = match + index
        except ValueError:
            pos = match + 1
    return json_objects


def extract_image_uri(response_str):
    pattern = r'"image_uri":\s*"([^"]+)"'
    match = re.search(pattern, response_str)
    return match.group(1) if match else None


def extract_file_uri(response_str):
    pattern = r'"file_uri":\s*"([^"]+)"'
    match = re.search(pattern, response_str)
    return match.group(1) if match else None


def generate_random_audio_filename(extension="mp3"):
    uuid1 = str(uuid.uuid4())
    uuid2 = str(uuid.uuid4())
    filename = f"generated_audio_{uuid1}_{uuid2}.{extension}"
    return filename


def step_back_retry_mechanism(client, latest_message, caller="respond"):
    from apps.core.generative_ai.utils import RetryCallersNames, DEFAULT_ERROR_MESSAGE
    if apps.core.generative_ai.utils.constant_utils.ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:
        apps.core.generative_ai.utils.constant_utils.ACTIVE_RETRY_COUNT += 1
        if caller == RetryCallersNames.RESPOND:
            return client.respond(latest_message=latest_message)
        elif caller == RetryCallersNames.RESPOND_STREAM:
            return client.respond_stream(latest_message=latest_message)
        else:
            return DEFAULT_ERROR_MESSAGE
    else:
        return DEFAULT_ERROR_MESSAGE
