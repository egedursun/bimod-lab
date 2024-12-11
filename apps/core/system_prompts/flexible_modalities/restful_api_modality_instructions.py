#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: build_apis_multimodality_prompt.py
#  Last Modified: 2024-10-05 02:26:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:35
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


import json

from apps.assistants.models import Assistant

from apps.mm_apis.models import (
    CustomAPIReference
)


def build_apis_multi_modality_prompt(assistant: Assistant):
    custom_api_references = CustomAPIReference.objects.filter(
        assistant=assistant
    )

    response_prompt = """
            ### **CUSTOM APIS:**

            '''
            """

    for i, custom_api_reference in enumerate(custom_api_references):
        custom_api = custom_api_reference.custom_api

        response_prompt += f"""
                [Custom API Reference ID: {custom_api_reference.id}]
                    API Name: {custom_api.name}
                    API Description: {custom_api.description}
                    API Base URL: {custom_api.base_url}
                    API Endpoints & Descriptions:
                    '''
                    {json.dumps(custom_api.endpoints, indent=4)}
                    '''
                """

    response_prompt += """
            ---

            '''

            **INFORMATION ABOUT THE AVAILABLE SOURCES AND FORMATS:**
            - This information is shared with you for you to have a clear understanding about the custom APIs. You can
            use this info to execute the custom APIs properly by providing the necessary input data and the API ID.

            - *Base URL:*
                - The base URL field will be shared as a string that represents the base URL of the API.

            - *Endpoints & Descriptions:*
                - The endpoints field will be shared as a dict where each key represents the endpoint name and the
                value represents the details about the endpoint in the following format:
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

            ---

            **NOTE**: You need to primarily choose an API you would like to use depending on the use case, and also
            the name of the endpoint you would like to use for the API. You can then provide the input data to get the
            desired output. The input data can be provided in the form of path parameters, query parameters, and body
            parameters as shown above.

            ---
            """

    return response_prompt


def build_semantor_apis_multi_modality_prompt(
    temporary_sources: dict
):

    custom_api_references = temporary_sources.get("tools").get("apis")

    response_prompt = """
            ### **CUSTOM APIS:**

            '''
            """

    for i, custom_api_reference in enumerate(custom_api_references):
        custom_api = custom_api_reference.custom_api

        response_prompt += f"""
                [Custom API Reference ID: {custom_api_reference.id}]
                    API Name: {custom_api.name}
                    API Description: {custom_api.description}
                    API Base URL: {custom_api.base_url}
                    API Endpoints & Descriptions:
                    '''
                    {json.dumps(custom_api.endpoints, indent=4)}
                    '''
                """

    response_prompt += """
            ---

            '''

            **INFORMATION ABOUT THE AVAILABLE SOURCES AND FORMATS:**
            - This information is shared with you for you to have a clear understanding about the custom APIs. You can
            use this info to execute the custom APIs properly by providing the necessary input data and the API ID.

            - *Base URL:*
                - The base URL field will be shared as a string that represents the base URL of the API.

            - *Endpoints & Descriptions:*
                - The endpoints field will be shared as a dict where each key represents the endpoint name and the
                value represents the details about the endpoint in the following format:
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

            ---

            **NOTE**: You need to primarily choose an API you would like to use depending on the use case, and also
            the name of the endpoint you would like to use for the API. You can then provide the input data to get the
            desired output. The input data can be provided in the form of path parameters, query parameters, and body
            parameters as shown above.

            ---
            """
    return response_prompt


def build_lean_apis_multi_modality_prompt():
    response_prompt = """
            **CUSTOM API CONNECTIONS:**

            '''
            <This information is redacted because you won't need it to serve your instructions.>
            '''

            **INFORMATION ABOUT THE AVAILABLE SOURCES AND FORMATS:**
            - This information is shared with you for you to have a clear understanding about the custom APIs. You can
            use this info to execute the custom APIs properly by providing the necessary input data and the API ID.

            - *Base URL:*
                - The base URL field will be shared as a string that represents the base URL of the API.

            - *Endpoints & Descriptions:*
                - The endpoints field will be shared as a dict where each key represents the endpoint name and the
                value represents the details about the endpoint in the following format:
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

            ---

            **NOTE**: You need to primarily choose an API you would like to use depending on the use case, and also
            the name of the endpoint you would like to use for the API. You can then provide the input data to get the
            desired output. The input data can be provided in the form of path parameters, query parameters, and body
            parameters as shown above.

            ---
            """

    return response_prompt
