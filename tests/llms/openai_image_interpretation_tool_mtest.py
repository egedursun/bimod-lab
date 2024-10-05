#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#

import time
import base64 as b64

import boto3
from openai import OpenAI

from apps._services.llms.helpers.helper_prompts import HELPER_ASSISTANT_PROMPTS
from config import settings

"""
    #################################################################################################################
    THIS TEST IS OUTDATED AND SHOULD BE UPDATED TO REFLECT THE CURRENT IMPLEMENTATION OF THE IMAGE INTERPRETATION TOOL.
    #################################################################################################################
"""


#######################################################################################################################
# ENUMERATIONS
#######################################################################################################################

class ChatRoles:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AssistantRunStatuses:
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REQUIRES_ACTION = "requires_action"
    EXPIRED = "expired"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    FAILED = "failed"
    INCOMPLETE = "incomplete"

#######################################################################################################################
#######################################################################################################################


def ask_about_image(client, full_image_paths: list, query_string: str):

    # start timer
    timer_start = time.time()

    if len(full_image_paths) > 20:
        return ("System Message: The number of images to be interpreted is too high. Please provide a smaller "
                "number of images. The maximum number supported by the system is 20.")

    image_contents = []
    for path in full_image_paths:
        if not path:
            return "System Message: The image path is empty."

        try:
            # Read binary image contents from s3
            boto3_client = boto3.client('s3')
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            image_bytes = boto3_client.get_object(Bucket=bucket_name, Key=path)["Body"].read()
            extension = path.split(".")[-1]
            image_contents.append({"binary": image_bytes, "extension": extension})
        except FileNotFoundError:
            print(f"System Message: The image at the path '{path}' could not be found, skipping image...")
            continue
        except Exception as e:
            print(f"System Message: An error occurred while reading the image at the path '{path}', "
                  f"skipping image...")
            print(f"Error Details: {str(e)}")
            continue

    # Convert binaries to base64
    image_objects = []
    for image_content in image_contents:
        binary = image_content["binary"]
        extension = image_content["extension"]
        # convert to base64
        image_base64 = b64.b64encode(binary).decode("utf-8")
        image_objects.append({"base64": image_base64, "extension": extension})

    # Prepare the thread
    messages = [
        {"role": ChatRoles.SYSTEM, "content": [{"type": "text", "text": HELPER_ASSISTANT_PROMPTS["image_interpreter"]["description"]}]},
        {"role": ChatRoles.USER, "content": [{"type": "text","text": query_string}]}
    ]
    for image_object in image_objects:
        formatted_uri = f"data:image/{image_object['extension']};base64,{image_object['base64']}"
        messages[-1]["content"].append({"type": "image_url", "image_url": {"url": formatted_uri}})
    # END FOR

    # Retrieve the response from the assistant
    response = client.chat.completions.create(
        model=HELPER_ASSISTANT_PROMPTS["image_interpreter"]["model"],
        messages=messages,
        temperature=0.0,
        max_tokens=1024,
    )

    choices = response.choices
    first_choice = choices[0]
    choice_message = first_choice.message
    choice_message_content = choice_message.content
    print(choice_message_content)
    return choice_message_content


OPENAI_API_KEY = "sk-proj-AfSj7ohaxbXDQf2WLLSUT3BlbkFJGZifjSfVePMOJtBeRz5V"
image_path_1 = './test_image_1.png'
image_path_2 = './test_image_2.png'

c = OpenAI(api_key=OPENAI_API_KEY)

ask_about_image(c,
               [image_path_1, image_path_2],
               "Tell me what do you see in these images, explain the concepts and abstract ideas in them.")
