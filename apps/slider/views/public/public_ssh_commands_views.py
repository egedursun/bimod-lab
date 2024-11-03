#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: public_ssh_commands_views.py
#  Last Modified: 2024-10-31 03:07:19
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-31 03:07:20
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

from apps.core.slider.slider_executor_public import SliderExecutionManager_Public
from apps.slider.utils import is_valid_google_apps_authentication_key

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class SliderView_PublicGenerateViaSSHCommand(View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        command = request.POST.get('command')
        if command is None:
            logger.error(f"SSH Command is required.")
            return JsonResponse({"output": None, "message": "SSH Command is required."})

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

        xc = SliderExecutionManager_Public(slider_google_apps_connection=connection_object,
                                           text_content=text_content)
        response_json = xc.execute_ssh_command(command=command)
        logger.info(f"SSH Command was executed for Google Apps Connection: {connection_object}")
        return JsonResponse(response_json)
