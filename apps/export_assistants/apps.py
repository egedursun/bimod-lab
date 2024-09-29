#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: apps.py
#  Last Modified: 2024-08-07 16:37:57
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 22:50:56
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.apps import AppConfig

from config import settings


class ExportAssistantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.export_assistants'

    def ready(self):
        # Schedule the command to run after the server starts
        if settings.TESTING:
            return

        from threading import Thread
        from django.core.management import call_command

        def run_initialization_command():
            call_command('start_exported_assistants')

        # Use a separate thread to avoid blocking the server startup
        thread = Thread(target=run_initialization_command)
        thread.start()
