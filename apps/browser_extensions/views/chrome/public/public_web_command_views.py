#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: public_web_command_views.py
#  Last Modified: 2025-01-24 18:43:44
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-01-24 18:43:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import logging

from django.http import JsonResponse

from django.utils.decorators import (
    method_decorator
)

from django.views import View

from django.views.decorators.csrf import (
    csrf_exempt
)

from apps.core.browser_extensions.extensions.chrome.chrome_extension_executor_public import (
    ExtensionExecutionManager_Public
)

from apps.browser_extensions.utils import (
    is_valid_chrome_extension_connection_authentication_key
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class BrowserExtensionView_PublicGenerateViaWebCommand(View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        command = request.POST.get('command')

        if command is None:
            logger.error(f"Web Command is required.")

            return JsonResponse(
                {
                    "output": None,
                    "message": "Web Command is required."
                }
            )

        text_content = request.POST.get('text_content')

        if text_content is None:
            logger.error(f"Text Content is None, assuming empty string.")
            text_content = ""

        # auth key check

        authentication_key = request.POST.get('authentication_key')

        if authentication_key is None:
            logger.error(f"Google Apps Authentication Key is required.")

            return JsonResponse(
                {
                    "output": None,
                    "message": "Google Apps Authentication Key is required."
                }
            )

        connection_object = is_valid_chrome_extension_connection_authentication_key(
            authentication_key=authentication_key
        )

        if not connection_object:
            logger.error(f"Invalid Google Apps Authentication Key.")

            return JsonResponse(
                {
                    "output": None,
                    "message": "Invalid Google Apps Authentication Key."
                }
            )

        xc = ExtensionExecutionManager_Public(
            extension_google_apps_connection=connection_object,
            text_content=text_content
        )

        response_json = xc.execute_web_command(
            command=command
        )

        logger.info(f"Web Command was executed for Google Apps Connection: {connection_object}")

        return JsonResponse(response_json)
