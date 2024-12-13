#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-09 19:29:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:29:10
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib.admin.models import (
    LogEntry
)

from apps.audit_logs.models import (
    AuditLog
)

HTTP_STATUS_QUERY_TAG = 'http_status'
HTTP_STATUS_ERROR_TAG_VALUE = 'error'

EXCLUDE_MODELS_FROM_AUDIT_LOGS = [
    AuditLog,
    LogEntry
]
