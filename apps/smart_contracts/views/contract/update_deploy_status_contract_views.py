#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: update_deploy_status_contract_views.py
#  Last Modified: 2024-10-21 02:00:17
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 02:00:17
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
from django.views import View

from apps.core.smart_contracts.smart_contracts_executor import SmartContractsExecutionManager
from apps.smart_contracts.models import BlockchainSmartContract
from apps.smart_contracts.utils import DeploymentStatusesNames

logger = logging.getLogger(__name__)


class SmartContractView_ContractUpdateDeployStatus(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        contract_id = kwargs.get('pk')
        contract_object: BlockchainSmartContract = BlockchainSmartContract.objects.get(id=contract_id)

        # NOT STAGED YET
        if contract_object.tx_hash is None:
            logger.info(f"This contract is not yet staged for deployment. Please proceed with the deployment "
                        f"process to check the updates.")
            messages.error(request, f"This contract is not yet staged for deployment. Please proceed with "
                                    f"the deployment process to check the updates.")
            return redirect('smart_contracts:contract_list')

        # ALREADY DEPLOYED
        if contract_object.deployment_status == DeploymentStatusesNames.DEPLOYED:
            logger.info(f"This contract is already deployed. Please check the transaction receipt details of "
                        f"the contract.")
            messages.error(request, f"This contract is already deployed. Please check the transaction receipt "
                                    f"details of your contract.")
            return redirect('smart_contracts:contract_list')

        # CHECKING PERMISSION GRANTED: DEPLOYMENT ONGOING
        status, error = SmartContractsExecutionManager.check_deployment_status(contract_obj=contract_object)

        if error is not None:
            messages.warning(request, f"No updates found for the contract deployment status (yet).")
            return redirect('smart_contracts:contract_list')
        return redirect('smart_contracts:contract_list')

        if status is True:
            logger.info(f"The smart contract has been deployed successfully. Please check the transaction "
                        f"receipt for details.")
            messages.success(request, f"Your contract has been deployed successfully. Please check the "
                                      f"transaction receipt for details.")
            return redirect('smart_contracts:contract_list')

        messages.error(request, f"An error occurred while checking the deployment status of your contract. "
                                f"Please try again later.")
        return redirect('smart_contracts:contract_list')
