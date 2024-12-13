#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: regenerate_node_api_key_views.py
#  Last Modified: 2024-10-18 19:02:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-18 19:02:14
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import secrets

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.http import JsonResponse
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.hadron_prime.models import HadronNode

from apps.hadron_prime.utils import (
    HADRON_NODE_AUTHENTICATION_KEY_TOKEN_SIZE
)

import logging

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class HadronPrimeView_RegenerateNodeApiKey(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        node_id = kwargs.get('pk')

        ##############################
        # PERMISSION CHECK FOR - UPDATE_HADRON_NODES
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.UPDATE_HADRON_NODES
        ):
            messages.error(self.request, "You do not have permission to regenerate API Key for Hadron Node.")
            return JsonResponse({'error': 'You do not have permission to regenerate API Key for Hadron Node.'})
        ##############################

        node = HadronNode.objects.get(
            id=node_id
        )

        new_token = str(
            secrets.token_urlsafe(
                HADRON_NODE_AUTHENTICATION_KEY_TOKEN_SIZE
            )
        )

        node.activation_trigger_authentication_key = new_token

        logger.info(f"New Node API Key regenerated for node: {node.node_name}")

        node.save()

        return JsonResponse(
            {
                'new_token': new_token
            }
        )
