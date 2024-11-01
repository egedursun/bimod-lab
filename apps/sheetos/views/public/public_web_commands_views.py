#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: public_web_commands_views.py
#  Last Modified: 2024-10-31 05:36:06
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 19:29:12
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
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.core.sheetos.sheetos_executor_public import SheetosExecutionManager_Public
from apps.sheetos.utils import is_valid_google_apps_authentication_key

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class SheetosView_PublicGenerateViaWebCommand(View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        command = request.POST.get('command')
        if command is None:
            logger.error(f"Web Command is required.")
            return JsonResponse({"output": None, "message": "Web Command is required."})

        text_content = request.POST.get('text_content')
        if text_content is None:
            logger.error(f"Text Content is None, assuming empty string.")
            text_content = ""

        # auth key check
        authentication_key = request.POST.get('authentication_key')
        if authentication_key is None:
            logger.error(f"Google Apps Authentication Key is required.")
            return JsonResponse({"output": None, "message": "Google Apps Authentication Key is required."})

        connection_object = is_valid_google_apps_authentication_key(authentication_key=authentication_key)
        if not connection_object:
            logger.error(f"Invalid Google Apps Authentication Key.")
            return JsonResponse({"output": None, "message": "Invalid Google Apps Authentication Key."})

        xc = SheetosExecutionManager_Public(sheetos_google_apps_connection=connection_object,
                                            text_content=text_content)
        response_json = xc.execute_web_command(command=command)
        logger.info(f"Web Command was executed for Google Apps Connection: {connection_object}")
        print("response_json: ", response_json)
        return JsonResponse(response_json)
