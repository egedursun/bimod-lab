#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: apps.py
#  Last Modified: 2024-09-15 15:15:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:14:54
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.apps import AppConfig


class MainAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        from data.loader import BoilerplateDataLoader
        BoilerplateDataLoader.load()
