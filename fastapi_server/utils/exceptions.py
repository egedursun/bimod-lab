#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: exceptions.py
#  Last Modified: 2025-02-01 22:25:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-01 22:25:52
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from starlette.responses import JSONResponse

from fastapi_server.utils import statuses


def raise_not_authorized_error(request):
    return JSONResponse(
        {
            "status": statuses.ERROR,
            "message": "You are not authorized to perform this operation.",
            "errors": {
                "message": "You are not authorized to perform this operation."
            },
            "meta": {
                "request": request.url.path,
                "method": request.method,
                "status_code": 403
            }
        }
    )
