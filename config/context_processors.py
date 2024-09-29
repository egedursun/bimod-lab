#  Copyright (c) 2024 BMD® Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io
#  File: context_processors.py
#  Last Modified: 2024-06-20 04:48:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD® Autonomous Holdings)
#  Created: 2024-09-28 23:15:08
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD® Autonomous Holdings.
#
#  For permission inquiries, please contact: admin@bimod.io.

from django.conf import settings


def my_setting(request):
    return {'MY_SETTING': settings}


def language_code(request):
    return {"LANGUAGE_CODE": request.LANGUAGE_CODE}


def get_cookie(request):
    return {"COOKIES": request.COOKIES}


# Add the 'ENVIRONMENT' setting to the template context
def environment(request):
    return {'ENVIRONMENT': settings.ENVIRONMENT}
