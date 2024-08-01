import json

from apps.assistants.models import Assistant
from apps.mm_apis.models import CustomAPIReference


def build_apis_multi_modality_prompt(assistant: Assistant):
    # Retrieve the functions of the assistant
    custom_api_references = CustomAPIReference.objects.filter(assistant=assistant)
    # Build the prompt
    response_prompt = """
            **CUSTOM API CONNECTIONS:**

            '''
            """

    for i, custom_api_reference in enumerate(custom_api_references):
        custom_api = custom_api_reference.custom_api
        response_prompt += f"""
                [Custom API Reference ID: {custom_api_reference.id}]
                    Custom API Name: {custom_api.name}
                    Custom API Description: {custom_api.description}
                    API Base URL: {custom_api.base_url}
                    API Endpoints & Descriptions:
                    '''
                    {json.dumps(custom_api.endpoints, indent=4)}
                    '''
                """

    response_prompt += """
            -------

            '''

            **THE NOTE ABOUT THE FORMAT OF THE BASE URL, ENDPOINTS, AND DESCRIPTIONS ARE DELIVERED:**
            - This information is shared with you for you to have a more clear understanding about the custom APIs
            given in the system. You can use this information to execute the custom APIs properly by providing the
            necessary input data and the API ID more easily.

            *Base URL:*
            - The base URL field will be shared as a string that represents the base URL of the custom API.

            *Endpoints & Descriptions:*
            - The endpoints field will be shared as a dictionary where each key represents the endpoint name and the value
            represents the important details about the endpoint in the following format:
            '''
            {
                "Some Endpoint Name": {
                    "description": "Some natural language description explaining what this endpoint does.",
                    "path": "/users/{user_id}/details",
                    "method": "POST",
                    "header_params": ["Authorization"],
                    "path_params": ["user_id"],
                    "query_params": ["age", "sex"],
                    "body_params": ["name", "email", "password"]
                },
                "Other Endpoint Name" = {
                    ...
                }
            }
            '''

            -------

            **NOTE**: You need to primarily choose an API you would like to use depending on the use case, and also
            the name of the endpoint you would like to use for the API. You can then provide the necessary input data
            to the API to get the desired output. The input data can be provided in the form of path parameters, query
            parameters, and body parameters as shown in the endpoint details, and future explanations will be made
            on the relevant tool section of your prompt.

            -------
            """
    return response_prompt


def build_lean_apis_multi_modality_prompt():
    # Build the prompt
    response_prompt = """
            **CUSTOM API CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            **THE NOTE ABOUT THE FORMAT OF THE BASE URL, ENDPOINTS, AND DESCRIPTIONS ARE DELIVERED:**
            - This information is shared with you for you to have a more clear understanding about the custom APIs
            given in the system. You can use this information to execute the custom APIs properly by providing the
            necessary input data and the API ID more easily.

            *Base URL:*
            - The base URL field will be shared as a string that represents the base URL of the custom API.

            *Endpoints & Descriptions:*
            - The endpoints field will be shared as a dictionary where each key represents the endpoint name and the value
            represents the important details about the endpoint in the following format:
            '''
            {
                "Some Endpoint Name": {
                    "description": "Some natural language description explaining what this endpoint does.",
                    "path": "/users/{user_id}/details",
                    "method": "POST",
                    "header_params": ["Authorization"],
                    "path_params": ["user_id"],
                    "query_params": ["age", "sex"],
                    "body_params": ["name", "email", "password"]
                },
                "Other Endpoint Name" = {
                    ...
                }
            }
            '''

            -------

            **NOTE**: You need to primarily choose an API you would like to use depending on the use case, and also
            the name of the endpoint you would like to use for the API. You can then provide the necessary input data
            to the API to get the desired output. The input data can be provided in the form of path parameters, query
            parameters, and body parameters as shown in the endpoint details, and future explanations will be made
            on the relevant tool section of your prompt.

            -------
            """
    return response_prompt
