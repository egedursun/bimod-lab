#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: curl_parser.py
#  Last Modified: 2024-10-19 04:30:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 04:30:17
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging
import shlex
import requests

from apps.core.hadron_prime.utils import CURLHttpOptions, CURLHttpMethods

logger = logging.getLogger(__name__)


def parse_curl(curl_command):
    tokens = shlex.split(curl_command)
    method = 'GET'
    url = ''
    headers = {}
    data = None

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == 'curl':
            i += 1
            continue

        if (
            token.startswith(CURLHttpOptions.StartsWith.REQUEST) or
            token == CURLHttpOptions.Equals.REQUEST
        ):
            method = tokens[i + 1]
            i += 2
            continue

        if (
            token.startswith(CURLHttpOptions.StartsWith.HEADER) or
            token == CURLHttpOptions.Equals.HEADER
        ):
            header = tokens[i + 1]
            key, value = header.split(': ', 1)
            headers[key] = value
            i += 2
            continue

        if (
            token.startswith(CURLHttpOptions.StartsWith.DATA) or
            token == CURLHttpOptions.Equals.DATA or
            token == CURLHttpOptions.Equals.DATA_RAW
        ):
            data = tokens[i + 1]
            i += 2
            continue

        if token.startswith(CURLHttpOptions.StartsWith.URL):
            url = token
            i += 1
            continue
        i += 1

    if data:
        try:
            data = eval(data)

        except Exception as e:
            logger.error(f"Failed to parse data: {data}")
            pass

    return method, url, headers, data


def make_request_from_curl(curl_command):
    method, url, headers, data = parse_curl(curl_command)

    if method == CURLHttpMethods.GET:
        response = requests.get(url, headers=headers)

    elif method == CURLHttpMethods.POST:
        response = requests.post(url, headers=headers, data=data)

    elif method == CURLHttpMethods.PUT:
        response = requests.put(url, headers=headers, data=data)

    elif method == CURLHttpMethods.PATCH:
        response = requests.patch(url, headers=headers, data=data)

    elif method == CURLHttpMethods.DELETE:
        response = requests.delete(url, headers=headers)

    else:
        logger.error(f"Unsupported HTTP method: {method}")
        raise ValueError(f"Unsupported HTTP method: {method}")

    try:
        return response.text
        logger.info("Response is a valid JSON. Returning parsed response.")

    except ValueError:
        logger.warning("Response is not a valid JSON. Returning raw response.")
        return response.text
