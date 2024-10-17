#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: loading_bar_middleware.py
#  Last Modified: 2024-10-09 19:27:41
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-09 19:27:41
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

from config.consts.loading_bar_content import CONTENT_MIX


class LoadingBarMiddleware(MiddlewareMixin):
    def process_template_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            response.render()
            content = response.content.decode()
            loading_bar_html = CONTENT_MIX
            response.content = content.replace('</body>', loading_bar_html + '</body>')
        return response
