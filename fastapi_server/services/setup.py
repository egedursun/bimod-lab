#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: quick_setup.py
#  Last Modified: 2025-02-01 22:34:03
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-01 22:34:03
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from config.asgi import check_api_key

from fastapi_server.schemas.setup import (
    QuickSetupCreate
)

router = APIRouter(tags=["Setup"])


@router.post("/", name="setup")
def setup(request: Request, body: QuickSetupCreate):
    ux, e = check_api_key(request)

    if e:
        return e

    # Quick Setup Handler here.
    print(body)

    return JSONResponse(
        {
            "status": "success",
            "message": "Quick setup completed successfully.",
            "errors": {},
            "data": {},
            "meta": {
                "request": request.url.path,
                "method": request.method,
                "status_code": 200
            }
        }
    )
