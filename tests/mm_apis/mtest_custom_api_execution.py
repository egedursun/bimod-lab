

#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#

import requests

"""

    is_public = models.BooleanField(default=False)
    categories = models.JSONField(default=list, blank=True)

    name = models.CharField(max_length=255)
    description = models.TextField()

    authentication_type = models.CharField(max_length=5000, default="None", choices=CUSTOM_API_AUTHENTICATION_TYPES)
    authentication_key = models.CharField(max_length=5000, default="")
    base_url = models.CharField(max_length=5000, default="")
    endpoints = models.JSONField(default=dict, blank=True)

    custom_api_references = models.ManyToManyField("CustomAPIReference", blank=True)
    api_picture = models.ImageField(upload_to="custom_apis/%YYYY/%mm/%dd/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)

    is_featured = models.BooleanField(default=False)
"""

class AcceptedHTTPRequestMethods:
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


MAXIMUM_RETRIES = 3


def mm_api_execution_task(
    custom_api_id,
    endpoint_name: str,
    path_param_values: dict,
    query_param_values: dict,
    body_param_values: dict):

    authentication_type = "None"
    authentication_key = ""
    base_url = "https://cleanuri.com/api"
    endpoints = {
        "Shorten URL": {
            "path": "/v1/shorten",
            "description": "some",
            "method": "POST",
            "header_params": [],
            "path_params": [],
            "query_params": [],
            "body_params": ["url"]
        },
    }

    ####################################################################################################
    # IMPLEMENT THE STRATEGY
    ####################################################################################################

    response = {"stdout": "", "stderr": ""}

    # Build the request and endpoint URL
    url = base_url + endpoints[endpoint_name]["path"]

    # Add the path parameters if there is any
    if path_param_values:
        for key, value in path_param_values.items():
            url = url.replace("{" + key + "}", value)

    # Add the query parameters if there is any
    if query_param_values:
        url += "?"
        for key, value in query_param_values.items():
            url += key + "=" + value + "&"
        url = url[:-1]

    # Add the body parameters if there is any
    body = {}
    if body_param_values and endpoints[endpoint_name]["method"] in ["POST", "PUT"]:
        for key, value in body_param_values.items():
            body[key] = value

    # Add the headers to the request
    headers = {}
    if authentication_type == "Bearer":
        headers["Authorization"] = authentication_key

    # Decode the HTTP method and attempt the request
    if endpoints[endpoint_name]["method"] == AcceptedHTTPRequestMethods.GET:
        request_object = requests.Request(AcceptedHTTPRequestMethods.GET, url, headers=headers)
    elif endpoints[endpoint_name]["method"] == AcceptedHTTPRequestMethods.POST:
        request_object = requests.Request(AcceptedHTTPRequestMethods.POST, url, headers=headers, json=body)
    elif endpoints[endpoint_name]["method"] == AcceptedHTTPRequestMethods.PUT:
        request_object = requests.Request(AcceptedHTTPRequestMethods.PUT, url, headers=headers, json=body)
    elif endpoints[endpoint_name]["method"] == AcceptedHTTPRequestMethods.PATCH:
        request_object = requests.Request(AcceptedHTTPRequestMethods.PATCH, url, headers=headers, json=body)
    elif endpoints[endpoint_name]["method"] == AcceptedHTTPRequestMethods.DELETE:
        request_object = requests.Request(AcceptedHTTPRequestMethods.DELETE, url, headers=headers)
    else:
        response["stderr"] = "Unsupported HTTP method: " + endpoints[endpoint_name]["method"]
        return response

    # Prepare the request
    prepared_request = request_object.prepare()

    # Attempt the request and try 3 more times only if it fails
    for i in range(0, MAXIMUM_RETRIES):
        try:
            response_object = requests.Session().send(prepared_request)
            response["stdout"] = response_object.json()
            return response
        except Exception as e:
            response["stderr"] = str(e)
            continue

    return response


sample = mm_api_execution_task(
    custom_api_id=1,
    endpoint_name="Shorten URL",
    path_param_values={},
    query_param_values={},
    body_param_values={"url": "https://www.google.com"}
)
print(sample)
