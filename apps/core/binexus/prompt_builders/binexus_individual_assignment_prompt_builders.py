#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_individual_assignment_prompt_builders.py
#  Last Modified: 2024-10-22 23:46:10
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 23:46:11
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

from apps.core.binexus.prompts.binexus_individual_assignment_prompt import (
    binexus_individual_assignment_prompt,
    binexus_individual_assignment_prompt_redacted
)


def build_binexus_individual_assignment_prompt(
    process: BinexusProcess,
    individual
):
    merged_prompt = ""
    merged_prompt += binexus_individual_assignment_prompt(
        process=process,
        individual=individual
    )
    return merged_prompt


def build_binexus_individual_assignment_prompt_redacted(
    process: BinexusProcess,
    individual
):
    merged_prompt = ""
    merged_prompt += binexus_individual_assignment_prompt_redacted(
        process=process,
        individual=individual
    )
    return merged_prompt
