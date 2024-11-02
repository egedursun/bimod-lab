
#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-02 13:14:20
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
from json import JSONDecoder


logger = logging.getLogger(__name__)


def find_tool_call_from_json(response: str, decoder=JSONDecoder()):
    logger.info(f"Searching for tool call in response.")

    response = f"""{response}"""
    response = response.replace("\n", "").replace("'", '"').replace('```json', '').replace('```', '').replace('`', '')
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
