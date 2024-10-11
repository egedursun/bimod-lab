#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#
#
#
#

class ExportAPIStatusCodes:
    OK = 200
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    TOO_MANY_REQUESTS = 429
    SERVICE_OFFLINE = 503
    INTERNAL_SERVER_ERROR = 500


EXPORT_ASSISTANT_API_ADMIN_LIST = ("assistant", "is_public", "request_limit_per_hour", "created_by_user",
                                   "is_online", "created_at")
EXPORT_ASSISTANT_API_ADMIN_FILTER = ("assistant", "is_public", "request_limit_per_hour", "created_by_user",
                                     "is_online", "created_at")
EXPORT_ASSISTANT_API_ADMIN_SEARCH = ("assistant", "is_public", "request_limit_per_hour", "created_by_user",
                                     "is_online", "created_at")

EXPORT_ASSISTANT_LOG_ADMIN_LIST = ("export_assistant", "timestamp")
EXPORT_ASSISTANT_LOG_ADMIN_FILTER = ("export_assistant", "timestamp")
EXPORT_ASSISTANT_LOG_ADMIN_SEARCH = ("export_assistant", "timestamp")
