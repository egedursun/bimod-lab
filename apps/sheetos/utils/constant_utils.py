#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-31 18:31:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 18:31:01
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

SHEETOS_DOCUMENT_ADMIN_LIST = (
    'organization',
    'copilot_assistant',
    'document_folder',
    'document_title',
    'created_at',
    'created_by_user'
)
SHEETOS_DOCUMENT_ADMIN_LIST_FILTER = (
    'organization',
    'copilot_assistant',
    'document_folder',
    'created_at',
    'created_by_user'
)
SHEETOS_DOCUMENT_ADMIN_SEARCH = (
    'organization',
    'copilot_assistant',
    'document_folder',
    'document_title',
    'created_by_user'
)

SHEETOS_FOLDER_ADMIN_LIST = (
    'organization',
    'name',
    'description',
    'created_at',
    'created_by_user'
)
SHEETOS_FOLDER_ADMIN_FILTER = (
    'organization',
    'created_at',
    'created_by_user'
)
SHEETOS_FOLDER_ADMIN_SEARCH = (
    'organization',
    'name',
    'description'
)

SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_LIST = [
    'sheetos_assistant',
    'owner_user',
    'connection_api_key',
    'created_at',
    'updated_at'
]
SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_FILTER = [
    'sheetos_assistant',
    'owner_user',
    'created_at',
    'updated_at'
]
SHEETOS_GOOGLE_APPS_CONNECTION_ADMIN_SEARCH = [
    'sheetos_assistant',
    'owner_user',
    'connection_api_key'
]

SHEETOS_GOOGLE_APPS_CONNECTION_API_KEY_DEFAULT_LENGTH = 64
