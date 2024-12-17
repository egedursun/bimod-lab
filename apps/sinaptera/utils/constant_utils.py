#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-12-14 17:09:42
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 17:09:43
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

SINAPTERA_CONFIGURATION_ADMIN_LIST = (
    'user',
    'is_active_on_assistants',
    'is_active_on_leanmods',
    'is_active_on_orchestrators',
    'is_active_on_voidforgers',
    'rubric_weight_comprehensiveness',
    'rubric_weight_accuracy',
    'rubric_weight_relevancy',
    'rubric_weight_cohesiveness',
    'rubric_weight_diligence',
    'rubric_weight_grammar',
    'rubric_weight_naturalness',
    'branching_factor',
    'branch_keeping_factor',
    'evaluation_depth_factor',
    'additional_rubric_criteria',
    'created_at',
    'updated_at',
)
SINAPTERA_CONFIGURATION_ADMIN_FILTER = (
    'is_active_on_assistants',
    'is_active_on_leanmods',
    'is_active_on_orchestrators',
    'is_active_on_voidforgers',
    'rubric_weight_comprehensiveness',
    'rubric_weight_accuracy',
    'rubric_weight_relevancy',
    'rubric_weight_cohesiveness',
    'rubric_weight_diligence',
    'rubric_weight_grammar',
    'rubric_weight_naturalness',
    'branching_factor',
    'branch_keeping_factor',
    'evaluation_depth_factor',
    'created_at',
    'updated_at',
)
SINAPTERA_CONFIGURATION_ADMIN_SEARCH = (
    'user__username',
)
