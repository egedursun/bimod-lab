#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: mtest_json_1.py
#  Last Modified: 2024-10-05 20:35:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:08:39
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


def detect_tool_call(output: str, decoder=JSONDecoder()):
    objects_json_list = []
    output = output.replace("\n", "").replace("'", '"')
    pos = 0
    while True:
        match = output.find('{', pos)
        if match == -1:
            break
        try:
            res, idx = decoder.raw_decode(output[match:])
            objects_json_list.append(res)
            pos = match + idx
        except ValueError:
            pos = match + 1
    return objects_json_list
