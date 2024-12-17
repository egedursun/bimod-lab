#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: apps.py
#  Last Modified: 2024-11-16 18:33:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-15 22:57:45
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


class SemantorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.semantor'

    def ready(self):
        from apps.semantor.signals.update_assistant_embedding_signals import update_assistant_embedding_after_save
        from apps.semantor.signals.update_leanmod_assistant_embedding_signals import \
            update_leanmod_assistant_embedding_after_save
        from apps.semantor.signals.update_integration_embedding_signals import update_integration_embedding_after_save
        from apps.semantor.signals.delete_assistant_embedding_signals import \
            remove_vector_from_index_on_assistant_delete
        from apps.semantor.signals.delete_leanmod_assistant_embedding_signals import \
            remove_vector_from_index_on_leanmod_assistant_delete
        from apps.semantor.signals.delete_integration_embedding_signals import \
            remove_vector_from_index_on_integration_delete
        pass
