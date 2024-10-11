#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:41
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

class LeanModAssistantStatusCodes:
    OK = 200
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    TOO_MANY_REQUESTS = 429
    SERVICE_OFFLINE = 503
    INTERNAL_SERVER_ERROR = 500


EXPORT_LEANMOD_ASSISTANTS_API_ADMIN_LIST = ("lean_assistant", "is_public", "request_limit_per_hour",
                                            "created_by_user", "is_online", "created_at", "updated_at")
EXPORT_LEANMOD_ASSISTANTS_API_ADMIN_FILTER = ("lean_assistant", "is_public", "request_limit_per_hour",
                                              "created_by_user", "is_online", "created_at", "updated_at")
EXPORT_LEANMOD_ASSISTANTS_API_ADMIN_SEARCH = ("lean_assistant", "is_public", "request_limit_per_hour",
                                              "created_by_user", "is_online", "created_at", "updated_at")

EXPORT_LEANMOD_REQUEST_LOG_ADMIN_LIST = ("export_lean_assistant", "timestamp")
EXPORT_LEANMOD_REQUEST_LOG_ADMIN_FILTER = ("export_lean_assistant", "timestamp")
EXPORT_LEANMOD_REQUEST_LOG_ADMIN_SEARCH = ("export_lean_assistant", "timestamp")
