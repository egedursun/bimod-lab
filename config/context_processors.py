#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: context_processors.py
#  Last Modified: 2024-10-05 15:31:30
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 20:30:42
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.conf import settings


def my_setting(request):
    return {'MY_SETTING': settings}


def language_code(request):
    return {"LANGUAGE_CODE": request.LANGUAGE_CODE}


def get_cookie(request):
    return {"COOKIES": request.COOKIES}


def environment(request):
    return {'ENVIRONMENT': settings.ENVIRONMENT}
