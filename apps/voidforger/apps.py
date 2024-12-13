#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: apps.py
#  Last Modified: 2024-11-16 18:33:21
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-13 03:59:20
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


class VoidforgerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.voidforger'

    def ready(self):
        from apps.voidforger.signals import delete_toggle_auto_execution_memory_vector_embedding_signals
        from apps.voidforger.signals import delete_old_chat_messages_vector_embedding_signals
        from apps.voidforger.signals import delete_action_memory_vector_embedding_signals
        from apps.voidforger.signals import update_voidforger_toggle_auto_execution_memory_vector_embedding_after_save
        from apps.voidforger.signals import update_old_chat_messages_vector_embedding_signals
        from apps.voidforger.signals import update_action_memory_vector_embedding_signals
        pass
