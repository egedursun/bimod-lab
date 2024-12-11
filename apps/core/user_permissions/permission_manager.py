#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: permission_manager.py
#  Last Modified: 2024-10-05 02:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:37
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

from django.contrib.auth.models import User

from apps.user_permissions.models import (
    UserPermission
)

logger = logging.getLogger(__name__)


class UserPermissionManager:
    @staticmethod
    def is_authorized(
        user: User,
        operation: str
    ):
        user_permissions = UserPermission.active_permissions.filter(
            user=user
        ).all().values_list(
            'permission_type',
            flat=True
        )

        if operation not in user_permissions:
            logger.warning(f"User: {user.username} is not authorized to perform operation: {operation}")

            return False

        logger.info(f"User: {user.username} is authorized to perform operation: {operation}")

        return True
