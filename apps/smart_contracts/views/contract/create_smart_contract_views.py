#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: create_smart_contract_views.py
#  Last Modified: 2024-10-19 22:33:09
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-19 22:33:09
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
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.organization.models import Organization
from apps.smart_contracts.models import BlockchainWalletConnection, BlockchainSmartContract
from apps.smart_contracts.utils import SMART_CONTRACT_CATEGORIES, SMART_CONTRACT_TEMPLATE_CHOICES
from config.settings import SMART_CONTRACT_CREATION
from web_project import TemplateLayout
from apps.smart_contracts.utils import DeploymentStatusesNames

logger = logging.getLogger(__name__)


class SmartContractView_ContractCreate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['organizations'] = Organization.objects.filter(users__in=[self.request.user])
        context['wallet_connections'] = BlockchainWalletConnection.objects.filter(
            organization__in=context['organizations'])
        context['contract_categories'] = SMART_CONTRACT_CATEGORIES
        context['contract_templates'] = SMART_CONTRACT_TEMPLATE_CHOICES
        context['SMART_CONTRACT_CREATION'] = round(float(SMART_CONTRACT_CREATION), 2)
        return context

    def post(self, request, *args, **kwargs):
        wallet_id = request.POST.get('wallet')
        category = request.POST.get('category')
        nickname = request.POST.get('nickname')
        description = request.POST.get('description')
        contract_template = request.POST.get('contract_template')
        refinement_iterations = request.POST.get('refinement_iterations')
        offchain_contract_seed = request.POST.get('offchain_contract_seed')

        maximum_gas_limit = request.POST.get('maximum_gas_limit')
        gas_price_gwei = request.POST.get('gas_price_gwei')

        if not all([wallet_id, category, contract_template]):
            logger.error('All fields are required.')
            messages.error(request, 'All fields are required.')
            return redirect('smart_contracts:contract_create')

        wallet = BlockchainWalletConnection.objects.get(id=wallet_id)
        created_by_user = request.user
        smart_contract = BlockchainSmartContract.objects.create(
            wallet=wallet, category=category, contract_template=contract_template,
            nickname=nickname, description=description, refinement_iterations_before_evaluation=refinement_iterations,
            created_by_user=created_by_user, deployment_status=DeploymentStatusesNames.NOT_GENERATED, deployed_at=None,
            maximum_gas_limit=maximum_gas_limit, gas_price_gwei=gas_price_gwei,
            offchain_contract_seed=offchain_contract_seed)

        logger.info(f'Smart contract created successfully. Smart Contract ID: {smart_contract.id}')
        messages.success(request, 'Smart contract created successfully.')
        return redirect('smart_contracts:contract_list')
