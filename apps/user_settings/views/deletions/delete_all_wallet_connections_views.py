#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_all_wallet_connections_views.py
#  Last Modified: 2024-10-19 22:57:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:57:24
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

from django.contrib import messages

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.shortcuts import redirect
from django.views import View

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.smart_contracts.models import (
    BlockchainWalletConnection
)

from apps.user_permissions.utils import (
    PermissionNames
)

logger = logging.getLogger(__name__)


class SettingsView_DeleteAllWalletConnections(View, LoginRequiredMixin):
    def post(self, request, *args, **kwargs):

        user = request.user

        wallet_connections = BlockchainWalletConnection.objects.filter(
            assistant__organization__users__in=[user]
        ).all()

        confirmation_field = request.POST.get('confirmation', None)

        if confirmation_field != 'CONFIRM DELETING ALL BLOCKCHAIN WALLET CONNECTIONS':
            messages.error(request, "Invalid confirmation field. Please confirm the deletion by typing "
                                    "exactly 'CONFIRM DELETING ALL BLOCKCHAIN WALLET CONNECTIONS'.")
            logger.error(f"Invalid confirmation field: {confirmation_field}")

            return redirect('user_settings:settings')

        ##############################
        # PERMISSION CHECK FOR - DELETE_BLOCKCHAIN_WALLET_CONNECTIONS
        if not UserPermissionManager.is_authorized(
            user=self.request.user,
            operation=PermissionNames.DELETE_BLOCKCHAIN_WALLET_CONNECTIONS
        ):
            messages.error(self.request, "You do not have permission to delete blockchain wallet connections.")

            return redirect('user_settings:settings')
        ##############################

        try:
            for wallet_connection in wallet_connections:
                wallet_connection.delete()

            messages.success(request, "All blockchain wallet connections associated with your account have "
                                      "been deleted.")

            logger.info(f"All blockchain wallet connections associated with User: {user.id} have been deleted.")

        except Exception as e:
            messages.error(request, f"Error deleting blockchain wallet connections: {e}")
            logger.error(f"Error deleting blockchain wallet connections: {e}")

        return redirect('user_settings:settings')
