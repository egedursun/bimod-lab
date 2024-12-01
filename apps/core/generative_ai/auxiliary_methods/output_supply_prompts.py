#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: helper_prompts.py
#  Last Modified: 2024-10-05 02:20:19
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

class AgentRunConditions:
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REQUIRES_ACTION = "requires_action"
    EXPIRED = "expired"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"
    FAILED = "failed"
    INCOMPLETE = "incomplete"


BALANCE_OVERFLOW_LOG = f"""
    **SYSTEM MESSAGE:**
    - It seems like you don't have enough balance to continue this conversation. Please contact your organization's
    administrator to top up your balance, or if you have the necessary permissions, you can top up your balance
    yourself. If you encounter any problems during the balance top-up process, please connect the support team to
    get guidance.
"""

EMPTY_OBJECT_PATH_LOG = f"""
    **SYSTEM MESSAGE:**
    - The specified object path is not valid or NULL (empty).
"""
