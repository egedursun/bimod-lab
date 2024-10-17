#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

ML_MODEL_ITEM_CATEGORIES = (
    ('pth', 'PyTorch Model'),
)

ML_MODEL_ITEM_ADMIN_LIST = ('id', 'ml_model_base', 'ml_model_name', 'description', 'ml_model_size', 'full_file_path',
                            'created_at', 'updated_at')
ML_MODEL_ITEM_ADMIN_FILTER = ('ml_model_base',)
ML_MODEL_ITEM_ADMIN_SEARCH = ('ml_model_name', 'full_file_path')

ML_MODEL_MANAGER_ADMIN_LIST = ('id', 'assistant', 'name', 'model_object_category', 'directory_full_path', 'created_at',
                               'updated_at')
ML_MODEL_MANAGER_ADMIN_FILTER = ('assistant', 'model_object_category')
ML_MODEL_MANAGER_ADMIN_SEARCH = ('name', 'directory_full_path')

DELETE_ALL_ML_ITEMS_SPECIFIER = 'delete_all'
