#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: content_type_middleware.py
#  Last Modified: 2024-11-29 17:47:08
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-29 17:47:09
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.utils.deprecation import MiddlewareMixin


class ContentTypeMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path.endswith("manifest.json"):
            response["Content-Type"] = "application/json"
        return response
