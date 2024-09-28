import requests
from celery import shared_task

from apps.mm_apis.utils import MAXIMUM_RETRIES


@shared_task
def mm_api_execution_task(custom_api_id, endpoint_name: str, path_values=None, query_values=None, body_values=None):
    if path_values is None:
        path_values = {}
    from apps.mm_apis.models import CustomAPI
    from apps.mm_apis.utils import AcceptedHTTPRequestMethods

    response = {"stdout": "", "stderr": ""}
    custom_api = CustomAPI.objects.get(id=custom_api_id)
    authentication_type = custom_api.authentication_type
    authentication_key = custom_api.authentication_token
    base_url = custom_api.base_url
    endpoints = custom_api.endpoints

    # Build the request and endpoint URL
    url = base_url + endpoints[endpoint_name]["path"]

    # Add the path parameters if there is any
    if path_values:
        for key, value in path_values.items():
            url = url.replace("{" + key + "}", value)

    # Add the query parameters if there is any
    if query_values:
        url += "?"
        for key, value in query_values.items():
            url += key + "=" + value + "&"
        url = url[:-1]

    # Add the body parameters if there is any
    body = {}
    if body_values and endpoints[endpoint_name]["method"] in ["POST", "PUT"]:
        for key, value in body_values.items():
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

    # Attempt the request and try N times only if it fails
    for i in range(0, MAXIMUM_RETRIES):
        try:
            response_object = requests.Session().send(prepared_request)
            response["stdout"] = response_object.json()
            return response
        except Exception as e:
            response["stderr"] = str(e)
            continue
    return response
