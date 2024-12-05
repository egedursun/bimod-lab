#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: apps.py
#  Last Modified: 2024-10-12 01:08:39
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-03 14:35:18
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


class DatasourceNosqlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.datasource_nosql'

    def ready(self):
        from apps.datasource_nosql.signals.update_nosql_database_vector_embedding_signals import (
            update_nosql_database_vector_embedding_after_save
        )

        from apps.datasource_nosql.signals.delete_nosql_database_vector_embedding_signals import (
            remove_vector_from_index_on_nosql_database_delete
        )
