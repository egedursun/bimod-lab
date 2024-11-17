#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: apps.py
#  Last Modified: 2024-10-05 12:51:58
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:38
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


class AssistantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.assistants'

    def ready(self):
        from apps.assistants.signals.update_old_assistant_chat_messages_vector_embedding_signals import \
            update_assistant_old_chat_messages_vector_embedding_after_save
        from apps.assistants.signals.delete_old_assistant_chat_messages_vector_embedding_signals import \
            remove_vector_from_index_on_assistant_chat_message_delete
