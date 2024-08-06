import json
import re
from json import JSONDecoder


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
