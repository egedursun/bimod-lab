#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Br6.in™
#  File: apps.py
#  Last Modified: 2024-10-05 15:31:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:25:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@br6.in.
#

from django.apps import AppConfig
from django.apps import apps
from django.db.models.signals import pre_save, post_save, post_delete


class MainAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        from data.loader import BoilerplateDataLoader
        BoilerplateDataLoader.load()

        from .signals import log_save, log_delete
        for model in apps.get_models():
            post_save.connect(log_save, sender=model)
            post_delete.connect(log_delete, sender=model)
        print("[MainAppConfig.ready]: The AuditLogs tracking system have been successfully registered.")
