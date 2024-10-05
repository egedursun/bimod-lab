#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Jupi.tr™
#  File: fine_tuning_mtest.py
#  Last Modified: 2024-10-04 11:16:13
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

from pprint import pprint

from openai import OpenAI

####################################################################################################
TRAIN = False
####################################################################################################

openai_api_key = '...'

client = OpenAI(api_key=openai_api_key)

if TRAIN is True:

    training_file = "file-mydata"
    model_to_train = "gpt-3.5-turbo"

    # Create a file
    file = client.files.create(
          file=open("mydata.jsonl", "rb"),
          purpose="fine-tune"
        )

    # Create a fine-tuning run
    client.fine_tuning.jobs.create(
      training_file=file.id,
      model=model_to_train,
    )
else:
    pprint(client.fine_tuning.jobs.list(limit=10))

    model_name = "ft:gpt-3.5-turbo-0125:ross::A22K3HBq"
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "How are you?"},
        ]
    )
    print(completion.choices[0].message.content)
