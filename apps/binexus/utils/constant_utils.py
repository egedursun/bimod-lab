#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-22 02:02:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 02:02:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


BINEXUS_ELITE_AGENT_ADMIN_LIST = [
    'agent_nickname',
    'binexus_process',
    'binexus_fitness_score',
    'created_at'
]
BINEXUS_ELITE_AGENT_ADMIN_FILTER = [
    'binexus_process',
    'binexus_fitness_score',
    'created_at'
]
BINEXUS_ELITE_AGENT_ADMIN_SEARCH = [
    'agent_nickname',
    'binexus_process',
    'binexus_fitness_score',
    'created_at'
]

BINEXUS_PROCESS_ADMIN_LIST = [
    'process_name',
    'organization',
    'llm_model',
    'created_by_user',
    'created_at'
]
BINEXUS_PROCESS_ADMIN_FILTER = [
    'organization',
    'llm_model',
    'created_by_user'
]
BINEXUS_PROCESS_ADMIN_SEARCH = [
    'process_name',
    'organization__name',
    'llm_model__nickname',
    'created_by_user__username'
]
