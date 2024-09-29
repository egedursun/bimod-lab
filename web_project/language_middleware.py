#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: language_middleware.py
#  Last Modified: 2024-06-20 04:48:34
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:17:44
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.conf import settings
from django.utils.translation import activate


class DefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the django_language cookie is not set
        if 'django_language' not in request.COOKIES:
            # Get the default language from settings.LANGUAGE_CODE
            default_language = settings.LANGUAGE_CODE
            activate(default_language)
            response = self.get_response(request)
            response.set_cookie('django_language', default_language)

        else:
            response = self.get_response(request)

        return response
