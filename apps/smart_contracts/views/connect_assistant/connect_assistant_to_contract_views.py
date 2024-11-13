#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connect_assistant_to_contract_views.py
#  Last Modified: 2024-11-13 04:12:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 04:12:30
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
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.assistants.models import Assistant
from apps.core.user_permissions.permission_manager import UserPermissionManager
from apps.organization.models import Organization
from apps.smart_contracts.models import BlockchainSmartContract, SmartContractAssistantConnection
from apps.user_permissions.utils import PermissionNames
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SmartContractView_ConnectAssistantToSmartContract(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user_orgs = Organization.objects.filter(users__in=[self.request.user]).all()
        assistants = Assistant.objects.filter(organization__in=user_orgs).all()
        smart_contracts = BlockchainSmartContract.objects.filter(wallet__organization__in=user_orgs).all()
        context["assistants"] = assistants
        context["smart_contracts"] = smart_contracts
        context["existing_connections"] = SmartContractAssistantConnection.objects.filter(assistant__organization__in=user_orgs).all()
        return context

    def post(self, request, *args, **kwargs):
        assistant_id = self.request.POST.get("assistant_id")
        contract_id = self.request.POST.get("contract_id")

        ##############################
        # PERMISSION CHECK FOR - CONNECT_SMART_CONTRACTS_TO_ASSISTANT
        if not UserPermissionManager.is_authorized(user=self.request.user,
                                                   operation=PermissionNames.CONNECT_SMART_CONTRACTS_TO_ASSISTANT):
            messages.error(self.request, "You do not have permission to connect an assistant to a smart contract.")
            return self.render_to_response(self.get_context_data())
        ##############################

        assistant = Assistant.objects.get(id=assistant_id)
        smart_contract = BlockchainSmartContract.objects.get(id=contract_id)

        try:
            SmartContractAssistantConnection.objects.create(
                assistant=assistant,
                smart_contract=smart_contract,
                created_by_user=self.request.user
            )
        except Exception as e:
            messages.error(self.request, f"Error while connecting assistant to smart contract: {e}")
            logger.error(f"Error while connecting assistant to smart contract: {e}")

        messages.success(self.request, "Assistant connected to smart contract successfully.")
        return self.render_to_response(self.get_context_data())
