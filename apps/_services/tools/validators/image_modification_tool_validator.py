

def validate_image_modification_tool_json(tool_usage_json: dict):
    if "parameters" not in tool_usage_json:
        return """
            The 'parameters' field is missing from the tool_usage_json. This field is mandatory for using the Image
            Modification tool. Please make sure you are defining the 'parameters' field in the tool_usage_json.
        """
    parameters = tool_usage_json.get("parameters")

    if "prompt" not in parameters:
        return """
            The 'prompt' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory for
            using the Image Modification tool. Please make sure you are defining the 'prompt' field in the parameters field
            of the tool_usage_json.
        """

    if "image_size" not in parameters:
        return """
            The 'image_size' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Modification tool. Please make sure you are defining the 'file_paths' field in the parameters
            field of the tool_usage_json.
        """

    if "edit_image_uri" not in parameters:
        return """
            The 'edit_image_uri' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Modification tool. Please make sure you are defining the 'edit_image_uri' field in the parameters
            field of the tool_usage_json.
        """

    if "edit_image_mask_uri" not in parameters:
        return """
            The 'edit_image_mask_uri' field is missing from the 'parameters' field in the tool_usage_json. This field is mandatory
            for using the Image Modification tool. Please make sure you are defining the 'edit_image_mask_uri' field in the parameters
            field of the tool_usage_json.
        """
    return None
