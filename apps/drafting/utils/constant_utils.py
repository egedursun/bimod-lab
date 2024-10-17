#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-14 18:31:25
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-14 18:31:25
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


DRAFTING_DOCUMENT_ADMIN_LIST = ('organization', 'copilot_assistant', 'document_folder', 'document_title', 'created_at',
                                'created_by_user')
DRAFTING_DOCUMENT_ADMIN_LIST_FILTER = ('organization', 'copilot_assistant', 'document_folder', 'created_at',
                                       'created_by_user')
DRAFTING_DOCUMENT_ADMIN_SEARCH = ('organization', 'copilot_assistant', 'document_folder', 'document_title',
                                  'created_by_user')

DRAFTING_FOLDER_ADMIN_LIST = ('organization', 'name', 'description', 'created_at', 'created_by_user')
DRAFTING_FOLDER_ADMIN_FILTER = ('organization', 'created_at', 'created_by_user')
DRAFTING_FOLDER_ADMIN_SEARCH = ('organization', 'name', 'description')
