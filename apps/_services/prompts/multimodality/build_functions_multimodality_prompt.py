from apps.assistants.models import Assistant
from apps.mm_functions.models import CustomFunction, CustomFunctionReference


def build_functions_multimodality_prompt(assistant: Assistant):

    response_prompt = ""

    # Retrieve the functions of the assistant
    custom_function_references = CustomFunctionReference.objects.filter(assistant=assistant)

    # Build the prompt
    response_prompt = """
            **CUSTOM FUNCTIONS:**

            '''
            """

    for i, custom_function_reference in enumerate(custom_function_references):
        custom_function = custom_function_reference.custom_function
        response_prompt += f"""
                [Custom Function Reference ID: {custom_function_reference.id}]
                    Custom Function Name: {custom_function.name}
                    Custom Function Description: {custom_function.description}
                    Packages: {custom_function.packages}
                    Input Fields: {custom_function.input_fields}
                    Output Fields: {custom_function.output_fields}
                """

    response_prompt += """
            -------

            '''

            **THE NOTE ABOUT THE FORMAT OF THE PACKAGES, INPUT FIELDS, AND OUTPUT FIELDS ARE DELIVERED:**
            - This information is shared with you for you to have a more clear understanding about the custom functions
            given in the system. You can use this information to execute the custom functions properly by providing the
            necessary input data and the function ID more easily.

            *Packages:*
            - The packages field will be shared a list of dictionaries where each dictionary contains the name and version
                of the package:
                    {"name": "package_name", "version": "package_version"}
            - The version can also be None if it does not matter:
                    {"name": "package_name", "version": None}
            - The packages field can be empty if the function does not require any packages.
            - Even if the function requires a built-in package, it should be included in the packages field, otherwise
            the package will not be imported:
                    {"name": "random", "version": None}

            *Input Fields:*
            - The input fields will be shared as a list of dictionaries where each dictionary contains the name,
            description,type, and required fields:
                    {"name": "input_name", "description": "input_description_for_you_to_understand_more_context", "type": "input_data_type", "required": True/False}
            - The input data type can be string, integer, float, list, or dictionary, but it can't be an object.
            - If a field is not required, it can be left empty while calling the function.

            *Output Fields:*
            - The output fields will be shared as a list of dictionaries where each dictionary contains the name,
            description, and type fields:
                    {"name": "output_name", "description": "output_description_for_you_to_understand_more_context", "type": "output_data_type"}
            - The output data type can be string, integer, float, list, or dictionary, but it can't be an object.

            **NOTE**: The custom functions that are available in the system are defined by the system administrators
            and are available for execution in the system. You can call these functions properly by providing the
            necessary input data and the function ID.

            -------
            """

    return response_prompt
