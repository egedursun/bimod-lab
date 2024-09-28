def validate_image_generation_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Image
            Generation tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "prompt" not in parameters:
        return """
            The 'prompt' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Image Generation tool. Please make sure you are defining the 'prompt' field in the parameters field
            of the tool_usage_json.
        """

    if "size" not in parameters:
        return """
            The 'size' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Generation tool. Please make sure you are defining the 'file_paths' field in the parameters
            field of the tool_usage_json.
        """

    if "quality" not in parameters:
        return """
            The 'quality' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Image Generation tool. Please make sure you are defining the 'quality' field in the parameters field
            of the tool_usage_json.
        """
    print(f"[image_generation_tool_validator.validate_image_generation_tool_json] Validation is successful.")
    return None
