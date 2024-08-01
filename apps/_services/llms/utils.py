import json


def find_json_presence(response: str):
    json_objects = []
    brace_count = 0
    json_str = ""
    in_json = False

    for char in response:
        if char == '{':
            if brace_count == 0: in_json = True
            brace_count += 1
        if in_json: json_str += char
        if char == '}':
            brace_count -= 1
            if brace_count == 0:
                in_json = False
                try:
                    json.loads(json_str)
                    json_objects.append(json_str)
                except json.JSONDecodeError:
                    print(f"Invalid JSON found in the response: {json_str}")
                json_str = ""
    return json_objects if json_objects else None
