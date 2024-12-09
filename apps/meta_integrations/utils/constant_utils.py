#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-11-06 17:47:00
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-06 17:47:00
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


META_INTEGRATION_MANAGEMENT_TYPES = [
    ('expert_networks_and_lean_assistant', 'Expert Networks & Lean Assistant'),
    ('orchestration_maestro_and_lean_assistant', 'Orchestration Maestro & Lean Assistant'),
]


class MetaIntegrationManagementTypesNames:
    EXPERT_NETWORKS_AND_LEAN_ASSISTANT = 'expert_networks_and_lean_assistant'
    ORCHESTRATION_MAESTRO_AND_LEAN_ASSISTANT = 'orchestration_maestro_and_lean_assistant'

    @staticmethod
    def as_list():
        return [
            MetaIntegrationManagementTypesNames.EXPERT_NETWORKS_AND_LEAN_ASSISTANT,
            MetaIntegrationManagementTypesNames.ORCHESTRATION_MAESTRO_AND_LEAN_ASSISTANT
        ]


META_INTEGRATION_TEAM_ADMIN_LIST = [
    'meta_integration_name',
    'meta_integration_category',
    'created_at',
    'updated_at'
]
META_INTEGRATION_TEAM_ADMIN_FILTER = [
    'meta_integration_category',
    'created_at',
    'updated_at'
]
META_INTEGRATION_TEAM_ADMIN_SEARCH = [
    'meta_integration_name',
    'meta_integration_category'
]

META_INTEGRATION_CATEGORY_ADMIN_LIST = [
    'category_name',
    'category_description',
    'category_image_url',
    'created_at',
    'updated_at'
]
META_INTEGRATION_CATEGORY_ADMIN_FILTER = [
    'created_at',
    'updated_at'
]
META_INTEGRATION_CATEGORY_ADMIN_SEARCH = [
    'category_name'
]

META_INTEGRATION_ORCHESTRATOR_STANDARD_INSTRUCTIONS = f"""
    You are an orchestrator manager tasked to manage the team members assigned under your command,
    and organize and command your team members based on the requirements and queries of the user.
    Do your best in analyzing the capabilities of the assistants under your command, their tools and their
    strengths to decide which assistant to assign to which task. You are responsible for the success of the
    tasks assigned to you.
"""

META_INTEGRATION_LEANMOD_STANDARD_INSTRUCTIONS = f"""
    You are a lean assistant manager tasked to manage the team members assigned under your command,
    and organize and command your team members based on the requirements and queries of the user. You are
    capable of reaching to expert networks by understanding the strengths, tools, and capabilities of each of
    the assistants under your command. You are responsible for the success of the tasks assigned to you, and
    answering the queries of the user in the most efficient way possible.
"""
