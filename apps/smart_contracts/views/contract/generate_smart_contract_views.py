#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generate_smart_contract_views.py
#  Last Modified: 2024-10-20 23:20:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 23:20:29
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
from django.views.generic import TemplateView

from apps.core.smart_contracts.smart_contracts_executor import (
    SmartContractsExecutionManager
)

from apps.llm_core.models import LLMCore
from apps.organization.models import Organization

from apps.smart_contracts.models import (
    BlockchainSmartContract
)

from web_project import TemplateLayout

from apps.smart_contracts.utils import (
    GenerateSmartContractViewActionTypes,
    DeploymentStatusesNames
)

logger = logging.getLogger(__name__)


class SmartContractView_ContractGenerate(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        contract_id = kwargs.get('pk')

        user_orgs = Organization.objects.filter(
            users__in=[self.request.user]
        )

        contract = BlockchainSmartContract.objects.get(
            id=contract_id
        )

        llm_models = LLMCore.objects.filter(
            organization__in=user_orgs
        )

        context['contract'] = contract
        context['llm_models'] = llm_models
        return context

    def post(self, request, *args, **kwargs):
        contract_id = kwargs.get('pk')
        action_type = request.POST.get('action_type')

        contract_object: BlockchainSmartContract = BlockchainSmartContract.objects.get(
            id=contract_id
        )

        if action_type == GenerateSmartContractViewActionTypes.GENERATE_CONTRACT:
            original_prompt = request.POST.get('creation_prompt')
            previous_mistakes_prompt = request.POST.get('previous_mistakes_prompt', '')

            if original_prompt != contract_object.creation_prompt:
                contract_object.creation_prompt = original_prompt
                logger.info(f"Updated original_prompt for contract: {contract_object}")

                contract_object.save()

            llm_id = request.POST.get('llm_id')
            llm_core_model = LLMCore.objects.get(
                id=llm_id
            )

            try:
                xc = SmartContractsExecutionManager(
                    smart_contract_object=contract_object,
                    llm_model=llm_core_model
                )

            except Exception as e:
                messages.error(request, f"Error occurred while initializing SmartContractsExecutionManager: {e}")

                return redirect(
                    'smart_contracts:contract_generate',
                    pk=kwargs.get('pk')
                )

            response, error = xc.generate_contract_and_save_content(
                previous_mistakes_prompt=previous_mistakes_prompt
            )

            if (
                error is not None or
                response is False
            ):
                contract_object.deployment_status = DeploymentStatusesNames.FAILED

                contract_object.save()

                messages.error(request, f"Error occurred while generating the contract: {error}")

                return redirect(
                    'smart_contracts:contract_generate',
                    pk=kwargs.get('pk')
                )

            messages.success(request, f"Contract generated successfully.")

            return redirect(
                'smart_contracts:contract_generate',
                pk=kwargs.get('pk')
            )

        elif action_type == GenerateSmartContractViewActionTypes.SIGN_AND_DEPLOY_CONTRACT:

            response, error = SmartContractsExecutionManager.deploy_contract(
                contract_obj=contract_object
            )

            if (
                error is not None or
                response is False
            ):
                contract_object.deployment_status = DeploymentStatusesNames.FAILED

                contract_object.save()

                messages.error(request, f"Error occurred while signing and deploying the contract: {error}")

                return redirect(
                    'smart_contracts:contract_generate',
                    pk=kwargs.get('pk')
                )

            messages.success(request, f"Contract signed and deployed successfully.")

            return redirect(
                'smart_contracts:contract_generate',
                pk=kwargs.get('pk')
            )

        else:
            messages.error(request, f"Invalid action type: {action_type}")

            return redirect(
                'smart_contracts:contract_generate',
                pk=kwargs.get('pk')
            )
