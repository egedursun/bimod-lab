

def validate_image_variation_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Image
            Variation tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "image_uri" not in parameters:
        return """
            The 'image_uri' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Variation tool. Please make sure you are defining the 'image_uri' field in the parameters
            field of the tool_usage_json.
        """

    if "image_size" not in parameters:
        return """
            The 'image_size' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Variation tool. Please make sure you are defining the 'image_size' field in the parameters
            field of the tool_usage_json.
        """

    return None
