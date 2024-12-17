#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: list_smart_contracts_views.py
#  Last Modified: 2024-10-19 22:33:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:33:17
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

from django.contrib.auth.mixins import (
    LoginRequiredMixin
)

from django.views.generic import TemplateView

from apps.organization.models import Organization

from apps.smart_contracts.models import (
    BlockchainSmartContract
)

from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SmartContractView_ContractList(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context['contracts_by_org'] = self.get_smart_contracts_by_organization()

        return context

    def get_smart_contracts_by_organization(self):
        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        wallet_connections_by_org = {}

        for org in user_orgs:
            wallet_connections = BlockchainSmartContract.objects.filter(
                wallet__organization=org
            )

            wallet_connections_by_org[org] = wallet_connections

        return wallet_connections_by_org
