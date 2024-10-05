#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
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
