#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_execute_smart_contract_query.py
#  Last Modified: 2024-11-13 05:10:54
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:10:56
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

from apps.core.smart_contracts.smart_contracts_executor import (
    SmartContractsExecutionManager
)

from apps.llm_core.models import LLMCore

from apps.smart_contracts.models import (
    BlockchainSmartContract,
    BlockchainWalletConnection
)

from apps.smart_contracts.utils import (
    DeploymentStatusesNames
)

logger = logging.getLogger(__name__)


def run_query_execute_smart_contract_generation_query(
    user: User,
    llm_model: LLMCore,
    wallet_id: int,
    nickname: str,
    description: str,
    category: str,
    contract_template: str,
    creation_prompt: str,
    maximum_gas_limit: int,
    gas_price_gwei: int
):
    try:
        blockchain_wallet = BlockchainWalletConnection.objects.get(
            id=wallet_id
        )

        smart_contract_object = BlockchainSmartContract.objects.create(
            wallet=blockchain_wallet,
            nickname=nickname,
            description=description,
            category=category,
            contract_template=contract_template,
            contract_template_filepath="",
            creation_prompt=creation_prompt,
            maximum_gas_limit=maximum_gas_limit,
            gas_price_gwei=gas_price_gwei,
            created_by_user=user,
            deployment_status=DeploymentStatusesNames.NOT_GENERATED,
            deployed_at=None,
        )

        xc = SmartContractsExecutionManager(
            smart_contract_object=smart_contract_object,
            llm_model=llm_model
        )

        success, error = xc.generate_contract_and_save_content(
            previous_mistakes_prompt=None
        )

        if error is not None or success is False:
            logger.error(f"Error occurred while generating the smart contract content: {error}")

            smart_contract_object.deployment_status = DeploymentStatusesNames.FAILED
            smart_contract_object.save()

    except Exception as e:
        logger.error(f"Error occurred while generating the smart contract content: {e}")
        error = f"There has been an unexpected error while generating the smart contract content: {e}"

        return error

    return "Smart contract has been successfully generated."
