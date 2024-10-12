#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: function_utils.py
#  Last Modified: 2024-10-07 02:08:02
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-07 02:08:02
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
from json import JSONDecoder


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
