#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:47
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:40
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

NER_LANGUAGES = [
    ('en', 'English'),
]

NER_INTEGRATION_ADMIN_LIST = (
    'name',
    'organization',
    'language',
    'created_by_user',
    'created_at',
    'updated_at'
)
NER_INTEGRATION_ADMIN_SEARCH = (
    'name',
    'description'
)
NER_INTEGRATION_ADMIN_FILTER = (
    'organization',
    'language',
    'created_by_user'
)
