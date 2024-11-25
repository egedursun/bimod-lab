#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-24 20:06:51
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-24 20:06:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


class ExportVoidForgerRequestStatusCodes:
    OK = 200
    NOT_FOUND = 404
    UNAUTHORIZED = 401
    TOO_MANY_REQUESTS = 429
    SERVICE_OFFLINE = 503
    INTERNAL_SERVER_ERROR = 500


EXPORT_VOIDFORGER_ADMIN_LIST = (
    "voidforger",
    "is_public",
    "request_limit_per_hour",
    "created_by_user",
    "is_online",
    "created_at"
)
EXPORT_VOIDFORGER_ADMIN_FILTER = (
    "voidforger",
    "is_public",
    "request_limit_per_hour",
    "created_by_user",
    "is_online",
    "created_at",
)
EXPORT_VOIDFORGER_ADMIN_SEARCH = (
    "voidforger",
    "is_public",
    "request_limit_per_hour",
    "created_by_user",
    "is_online",
    "created_at"
)

EXPORT_VOIDFORGER_LOG_ADMIN_LIST = (
    "export_voidforger",
    "timestamp"
)
EXPORT_VOIDFORGER_LOG_ADMIN_FILTER = (
    "export_voidforger",
    "timestamp"
)
EXPORT_VOIDFORGER_LOG_ADMIN_SEARCH = (
    "export_voidforger",
    "timestamp"
)
