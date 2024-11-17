#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: delete_smart_contracts_views.py
#  Last Modified: 2024-10-19 22:33:26
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:33:27
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
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from apps.smart_contracts.models import BlockchainSmartContract
from web_project import TemplateLayout

logger = logging.getLogger(__name__)


class SmartContractView_ContractSoftDelete(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        contract_id = self.kwargs.get('pk')
        context['contract'] = get_object_or_404(BlockchainSmartContract, id=contract_id)
        return context

    def post(self, request, *args, **kwargs):
        contract_id = self.kwargs.get('pk')
        contract = get_object_or_404(BlockchainSmartContract, id=contract_id)

        try:
            contract.delete()
        except Exception as e:
            logger.error(f"An error occurred while soft-deleting the smart contract: {str(e)}")
            messages.error(request, f"An error occurred while soft-deleting the smart contract: {str(e)}")
            return redirect('smart_contracts:contract_detail', pk=contract_id)
        
        logger.info(f"Smart contract {contract_id} soft-deleted.")
        messages.success(request, f'Smart contract "{contract}" has been successfully deleted.')
        return redirect('smart_contracts:contract_list')
