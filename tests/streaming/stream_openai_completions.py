

#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: stream_openai_completions.py
#  Last Modified: 2024-10-03 12:42:16
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

from openai import OpenAI

openai_api_key = '...'

client = OpenAI(api_key=openai_api_key)


# send a ChatCompletion request to count to 100
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role': 'user', 'content': "Count to 100."},
    ],
    temperature=0,
    stream=True  # this time, we set stream=True
)


for chunk in response:
    choices = chunk.choices
    choice = choices[0]
    delta = choice.delta
    content = delta.content
    if content is not None:
        print(content, end='')
    else:
        continue
