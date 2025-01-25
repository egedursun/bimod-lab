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


from django.http import (
    HttpResponsePermanentRedirect
)


class AppendSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not request.path.endswith('/')

            and not request.path.startswith('/api/')

            and not request.path.startswith('/app/export_assistants/exported/')

            and not request.path.startswith('/app/export_assistants/health/')

            and not request.path.startswith('/app/export_leanmods/exported/')

            and not request.path.startswith('/app/mm_triggered_jobs/api/v1/webhook/*')

            and not request.path.startswith('/app/mm_triggered_jobs/orchestration/api/v1/webhook/*')

            and not request.path.startswith('/app/export_leanmods/health/')

            and not request.path.startswith('/app/export_orchestrations/exported/')

            and not request.path.startswith('/app/export_orchestrations/health/')

            and not request.path.startswith('/app/export_voidforger/exported/')

            and not request.path.startswith('/app/export_voidforger/health/')

            and not request.path.startswith('/app/export_voidforger/status/')

            and not request.path.startswith('/app/export_voidforger/manual_trigger/')

            and not request.path.startswith('/app/metakanban/meeting/recording/delivery')

            and not request.path.startswith('/app/metatempo/tempo/screenshot/delivery')

            and not request.path.startswith('/app/metatempo/tempo/connection/config')

            and not request.path.startswith('/app/drafting/public')

            and not request.path.startswith('/app/sheetos/public')

            and not request.path.startswith('/app/formica/public')

            and not request.path.startswith('/app/slider/public')

            and not request.path.startswith('/app/browser_extensions/public')

            and not request.path.startswith('/app/blog_app')

            and not request.path.startswith('/app/mobile_client')
        ):
            return HttpResponsePermanentRedirect(request.path + '/')

        return self.get_response(request)
