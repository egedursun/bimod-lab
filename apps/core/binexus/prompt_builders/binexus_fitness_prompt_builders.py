#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_fitness_prompt_builders.py
#  Last Modified: 2024-10-22 23:22:32
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 23:22:32
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.binexus.models import BinexusProcess

from apps.core.binexus.prompts import (
    binexus_generic_instructions_prompt,
    binexus_process_metadata_prompt,
    binexus_output_format_prompt,
    binexus_evaluation_individual_prompt
)


def build_binexus_fitness_evaluation_prompt(
    process: BinexusProcess,
    individual
):
    merged_prompt = ""

    merged_prompt += binexus_generic_instructions_prompt(
        process=process
    )

    merged_prompt += binexus_process_metadata_prompt(
        process=process
    )

    merged_prompt += binexus_output_format_prompt(
        process=process
    )

    merged_prompt += binexus_evaluation_individual_prompt(
        individual=individual
    )
    return merged_prompt
