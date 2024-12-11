#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_execute_smart_contract_function.py
#  Last Modified: 2024-10-22 00:21:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 00:21:15
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

from apps.assistants.models import Assistant

from apps.core.smart_contracts.smart_contracts_executor import (
    SmartContractsExecutionManager
)

from apps.smart_contracts.models import (
    BlockchainSmartContract
)

logger = logging.getLogger(__name__)


def execute_smart_contract_function_call(
    assistant_id: int,
    smart_contract_id: int,
    function_name: str,
    function_kwargs: dict
):
    agent: Assistant = Assistant.objects.get(
        id=assistant_id
    )

    smart_contract: BlockchainSmartContract = BlockchainSmartContract.objects.get(
        id=smart_contract_id
    )

    xc = SmartContractsExecutionManager(
        smart_contract_object=smart_contract,
        llm_model=agent.llm_model
    )

    try:
        output = xc.call_smart_contract_function(
            function_name=function_name,
            function_kwargs=function_kwargs
        )

        logger.info(f"Smart contract function call output: {output}")

    except Exception as e:
        error = f"Error occurred while executing smart contract function call: {e}"
        logger.error(f"Error occurred while executing smart contract function call: {e}")

        return error

    logger.info(f"Smart contract function call successful.")

    return output
