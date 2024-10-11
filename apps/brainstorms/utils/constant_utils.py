#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#


BRAINSTORMING_ADMIN_LIST = ('brainstorming_session', 'created_by_user', 'created_at')
BRAINSTORMING_ADMIN_FILTER = ('brainstorming_session', 'created_by_user', 'created_at')
BRAINSTORMING_ADMIN_SEARCH = ('brainstorming_session', 'created_by_user', 'created_at')

BRAINSTORMING_IDEA_ADMIN_LIST = ('idea_title', 'brainstorming_session', 'created_by_user', 'depth_level',
                                 'is_bookmarked', 'created_at')
BRAINSTORMING_IDEA_ADMIN_FILTER = ('brainstorming_session', 'created_by_user', 'depth_level', 'is_bookmarked',
                                   'created_at')
BRAINSTORMING_IDEA_ADMIN_SEARCH = ('idea_title', 'idea_description')

BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_LIST = ('brainstorming_session', 'depth_level', 'created_at')
BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_FILTER = ('brainstorming_session', 'depth_level', 'created_at')
BRAINSTORMING_LEVEL_SYNTHESIS_ADMIN_SEARCH = ('brainstorming_session', 'depth_level', 'created_at')

BRAINSTORMING_SESSION_ADMIN_LIST = ['session_name', 'organization', 'llm_model', 'created_by_user', 'created_at']
BRAINSTORMING_SESSION_ADMIN_FILTER = ['organization', 'llm_model', 'created_by_user', 'created_at']
BRAINSTORMING_SESSION_ADMIN_SEARCH = ['session_name', 'organization__name', 'llm_model__nickname',
                                      'created_by_user__username']


class BrainstormingActionTypeNames:
    CREATE_FIRST_LAYER = 'create_first_layer'
    CREATE_DEEPER_LAYER = 'create_deeper_layer'
    GENERATE_LEVEL_SYNTHESIS = 'generate_level_synthesis'
    GENERATE_COMPLETE_SYNTHESIS = 'generate_complete_synthesis'
