#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generate_contract_prompt_builder.py
#  Last Modified: 2024-10-21 00:30:13
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-21 00:30:13
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.core.smart_contracts.prompts import (
    contract_primary_instructions_prompt,
    contract_user_prompt_supply,
    contract_template_solidity_file_prompt,
    contract_offchain_seed_prompt,
    contract_metadata_prompt,
    contract_previous_mistakes_prompt,
    contract_refinement_primary_instructions,
    contract_syntactic_check_primary_instructions,
    contract_cost_effectiveness_primary_instructions,
    contract_final_evaluation_primary_instructions
)

from apps.smart_contracts.models import (
    BlockchainSmartContract
)


def build_smart_contract_generation_prompt(
    contract_object: BlockchainSmartContract,
    previous_mistakes_prompt
):
    merged_generation_prompt = ""

    merged_generation_prompt += contract_primary_instructions_prompt(
        contract_object=contract_object
    )

    merged_generation_prompt += contract_metadata_prompt(
        contract_object=contract_object
    )

    merged_generation_prompt += contract_user_prompt_supply(
        contract_object=contract_object
    )

    merged_generation_prompt += contract_template_solidity_file_prompt(
        contract_object=contract_object
    )

    merged_generation_prompt += contract_offchain_seed_prompt(
        contract_object=contract_object
    )

    if previous_mistakes_prompt is not None and previous_mistakes_prompt != "":
        merged_generation_prompt += contract_previous_mistakes_prompt(
            contract_object=contract_object,
            previous_mistakes_prompt=previous_mistakes_prompt
        )

    return merged_generation_prompt


def build_smart_contract_refinement_prompt(
    contract_object: BlockchainSmartContract,
    previous_mistakes_prompt
):
    merged_refinement_prompt = ""

    merged_refinement_prompt += contract_refinement_primary_instructions(
        contract_object=contract_object
    )

    merged_refinement_prompt += contract_syntactic_check_primary_instructions(
        contract_object=contract_object
    )

    merged_refinement_prompt += contract_cost_effectiveness_primary_instructions(
        contract_object=contract_object
    )

    merged_refinement_prompt += contract_final_evaluation_primary_instructions(
        contract_object=contract_object
    )

    if previous_mistakes_prompt is not None and previous_mistakes_prompt != "":
        merged_refinement_prompt += contract_previous_mistakes_prompt(
            contract_object=contract_object,
            previous_mistakes_prompt=previous_mistakes_prompt
        )

    return merged_refinement_prompt
