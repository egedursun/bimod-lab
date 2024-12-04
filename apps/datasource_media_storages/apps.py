#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: apps.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:48
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.apps import AppConfig


class DatasourceMediaStoragesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.datasource_media_storages'

    def ready(self):
        from apps.datasource_media_storages.signals.delete_old_media_item_vector_embedding_signals import (
            remove_vector_from_index_on_media_item_delete
        )

        from apps.datasource_media_storages.signals.update_old_media_item_vector_embedding_signals import (
            update_media_item_vector_embedding_after_save
        )
