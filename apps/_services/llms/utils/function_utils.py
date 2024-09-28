import re
import uuid
from json import JSONDecoder

import apps._services


def find_json_presence(response: str, decoder=JSONDecoder()):
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
    print("[utils.find_json_presence] Found JSON objects: ", json_objects)
    return json_objects


def extract_image_uri(response_str):
    # Regular expression pattern to match the image URI
    pattern = r'"image_uri":\s*"([^"]+)"'
    # Search for the pattern in the response string
    match = re.search(pattern, response_str)
    # Extract and return the URI if found, otherwise return None
    print("[utils.extract_image_uri] Image URI extracted.")
    return match.group(1) if match else None


def extract_file_uri(response_str):
    # Regular expression pattern to match the file URI
    pattern = r'"file_uri":\s*"([^"]+)"'
    # Search for the pattern in the response string
    match = re.search(pattern, response_str)
    # Extract and return the URI if found, otherwise return None
    print("[utils.extract_file_uri] File URI extracted.")
    return match.group(1) if match else None


def generate_random_audio_filename(extension="mp3"):
    # Generate a random filename
    uuid1 = str(uuid.uuid4())
    uuid2 = str(uuid.uuid4())

    filename = f"generated_audio_{uuid1}_{uuid2}.{extension}"
    print("[utils.generate_random_filename] Random filename generated.")
    return filename


def retry_mechanism(client, latest_message, caller="respond"):
    from apps._services.llms.utils import RetryCallersNames, DEFAULT_ERROR_MESSAGE

    if apps._services.llms.utils.constant_utils.ACTIVE_RETRY_COUNT < client.assistant.max_retry_count:
        apps._services.llms.utils.constant_utils.ACTIVE_RETRY_COUNT += 1
        if caller == RetryCallersNames.RESPOND:
            return client.respond(latest_message=latest_message)
        elif caller == RetryCallersNames.RESPOND_STREAM:
            return client.respond_stream(latest_message=latest_message)
        else:
            return DEFAULT_ERROR_MESSAGE
    else:
        return DEFAULT_ERROR_MESSAGE
