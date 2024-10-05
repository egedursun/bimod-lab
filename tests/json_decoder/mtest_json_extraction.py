
#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: mtest_json_extraction.py
#  Last Modified: 2024-08-07 16:37:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 01:37:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@jupi.tr.
#

from json import JSONDecoder


def find_json_presence(response: str, decoder=JSONDecoder()):
    json_objects = []
    response = response.replace("\n", "").replace("'", '"')
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


tool = {
    "tool": "Media Storage Query Execution",
    "parameters": {
        "media_storage_connection_id": 8,
        "type": "file_interpretation",
        "file_paths": [],
        "query": "Create an empty CSV file named empty_file.csv and store it locally."
    },
}


# Example usage
response_str = """Let's create an empty CSV file using the Media Storage Query Execution Tool. I'll make sure to provide the correct parameters.

    **Assistant Tool Call:**

    ```

    ['{\n    "tool": "Media Storage Query Execution",\n    "parameters": {\n        "media_storage_connection_id": 8,\n        "type": "file_interpretation",\n        "file_paths": [],\n        "query": "Create an empty CSV file named empty_file.csv and provide a download link."\n    }\n}']

    ```
"""

json_objects = find_json_presence(response_str)
for obj in json_objects:
    print(obj)
