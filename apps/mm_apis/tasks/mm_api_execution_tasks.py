#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: mm_api_execution_tasks.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:33
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

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
    auth_type = custom_api.authentication_type
    auth_key = custom_api.authentication_token
    base_url = custom_api.base_url
    endpoints = custom_api.endpoints
    url = base_url + endpoints[endpoint_name]["path"]
    if path_values:
        for key, value in path_values.items():
            url = url.replace("{" + key + "}", value)

    if query_values:
        url += "?"
        for key, value in query_values.items():
            url += key + "=" + value + "&"
        url = url[:-1]

    body = {}
    if body_values and endpoints[endpoint_name]["method"] in ["POST", "PUT"]:
        for key, value in body_values.items():
            body[key] = value

    headers = {}
    if auth_type == "Bearer":
        headers["Authorization"] = auth_key

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

    prep_req = request_object.prepare()
    for i in range(0, MAXIMUM_RETRIES):
        try:
            response_object = requests.Session().send(prep_req)
            response["stdout"] = response_object.json()
            return response
        except Exception as e:
            response["stderr"] = str(e)
            continue
    return response
