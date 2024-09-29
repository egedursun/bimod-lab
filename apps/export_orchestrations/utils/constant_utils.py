#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: constant_utils.py
#  Last Modified: 2024-09-28 15:08:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:52:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

class StatusCodes:
    """
    A simple class containing HTTP status codes used throughout the views.

    Attributes:
        OK (int): HTTP 200 OK.
        NOT_FOUND (int): HTTP 404 Not Found.
        UNAUTHORIZED (int): HTTP 401 Unauthorized.
        TOO_MANY_REQUESTS (int): HTTP 429 Too Many Requests.
        SERVICE_OFFLINE (int): HTTP 503 Service Unavailable.
        INTERNAL_SERVER_ERROR (int): HTTP 500 Internal Server Error.
    """
    OK = 200
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    TOO_MANY_REQUESTS = 429
    SERVICE_OFFLINE = 503
    INTERNAL_SERVER_ERROR = 500
