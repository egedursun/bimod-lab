#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: append_slash_middleware.py
#  Last Modified: 2024-10-09 19:27:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:27:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.http import HttpResponsePermanentRedirect


class AppendSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.path.endswith('/')
            and not request.path.startswith('/api/')
            and not request.path.startswith('/app/export_assistants/api/v1/export')
            and not request.path.startswith('/health/export_assistants/api/v1')
            and not request.path.startswith('/app/export_leanmods/api/v1/export')
            and not request.path.startswith('/health/export_leanmods/api/v1')
            and not request.path.startswith('/app/export_orchestrations/api/v1/export')
            and not request.path.startswith('/health/export_orchestrations/api/v1')
            and not request.path.startswith('/app/metakanban/meeting/recording/delivery')):
            return HttpResponsePermanentRedirect(request.path + '/')
        return self.get_response(request)
