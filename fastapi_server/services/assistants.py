#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: assistants.py
#  Last Modified: 2025-02-01 18:05:55
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2025-02-01 18:05:56
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import json

from django.core.serializers import serialize
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from apps.core.user_permissions.permission_manager import (
    UserPermissionManager
)

from apps.user_permissions.utils import PermissionNames
from fastapi_server.schemas.assistants import AssistantCreate

from fastapi_server.utils import statuses

from fastapi_server.utils.exceptions import (
    raise_not_authorized_error
)

router = APIRouter(tags=["Assistants"])


######################################################################################################################
# CREATE
######################################################################################################################
@router.post("/", name="create_assistant")
def create_assistant(request: Request, body: AssistantCreate):
    from apps.assistants.models import Assistant
    from config.asgi import check_api_key

    ux, e = check_api_key(request)
    if e:
        return e

    ##############################
    # PERMISSION CHECK FOR - ADD_ASSISTANTS
    if not UserPermissionManager.is_authorized(
        user=ux,
        operation=PermissionNames.ADD_ASSISTANTS
    ):
        return raise_not_authorized_error(request)
    ##############################

    try:
        assistant = Assistant.objects.create(
            **body.dict(),
        )

    except Exception as e:
        return JSONResponse(
            {
                "status": statuses.ERROR,
                "message": "An error occurred while creating the assistant.",
                "errors": {
                    "message": str(e)
                },
                "meta": {
                    "request": request.url.path,
                    "method": request.method,
                    "status_code": 500
                }
            }
        )

    return JSONResponse(
        {
            "status": statuses.SUCCESS,
            "message": "Assistant created successfully.",
            "errors": {},
            "data": json.loads(
                serialize(
                    "json",
                    [
                        assistant
                    ]
                )
            ),
            "meta": {
                "request": request.url.path,
                "method": request.method,
                "status_code": 201
            }
        }
    )


######################################################################################################################
# UPDATE
######################################################################################################################

@router.put("/{i_id}", name="update_assistant")
def update_assistant(i_id, request: Request, body: dict):
    from apps.assistants.models import Assistant
    from config.asgi import check_api_key

    ux, e = check_api_key(request)
    if e:
        return e

    ##############################
    # PERMISSION CHECK FOR - UPDATE_ASSISTANTS
    if not UserPermissionManager.is_authorized(
        user=ux,
        operation=PermissionNames.UPDATE_ASSISTANTS
    ):
        return raise_not_authorized_error(request)
    ##############################

    try:
        assistant = Assistant.objects.get(
            id=i_id,
            organization__users__in=[ux]
        )

        for k, v in body.items():
            setattr(assistant, k, v)

        assistant.save()

    except Exception as e:
        return JSONResponse(
            {
                "status": statuses.ERROR,
                "message": "An error occurred while updating the assistant.",
                "errors": {
                    "message": str(e)
                },
                "meta": {
                    "request": request.url.path,
                    "method": request.method,
                    "status_code": 500
                }
            }
        )

    return JSONResponse(
        {
            "status": statuses.SUCCESS,
            "message": "Assistant updated successfully.",
            "errors": {},
            "data": json.loads(
                serialize(
                    "json",
                    [
                        assistant
                    ]
                )
            ),
            "meta": {
                "request": request.url.path,
                "method": request.method,
                "status_code": 200
            }
        }
    )


######################################################################################################################
# GET ALL
######################################################################################################################

@router.get("/", name="get_all_assistants")
def get_all_assistants(request: Request):
    from apps.assistants.models import Assistant
    from config.asgi import check_api_key

    ux, e = check_api_key(request)
    if e:
        return e

    ##############################
    # PERMISSION CHECK FOR - LIST_ASSISTANTS
    if not UserPermissionManager.is_authorized(
        user=ux,
        operation=PermissionNames.LIST_ASSISTANTS
    ):
        return raise_not_authorized_error(request)
    ##############################

    try:
        assistants = Assistant.objects.filter(
            organization__users__in=[ux]
        ).all()

    except Exception as e:
        return JSONResponse(
            {
                "status": statuses.ERROR,
                "message": "An error occurred while fetching the assistants.",
                "errors": {
                    "message": str(e)
                },
                "meta": {
                    "request": request.url.path,
                    "method": request.method,
                    "status_code": 500
                }
            }
        )

    return JSONResponse(
        {
            "status": statuses.SUCCESS,
            "message": "Assistants fetched successfully.",
            "errors": {},
            "data": json.loads(
                serialize(
                    "json",
                    assistants
                )
            ),
            "meta": {
                "request": request.url.path,
                "method": request.method,
                "status_code": 200
            }
        }
    )


######################################################################################################################
# GET ONE
######################################################################################################################

@router.get("/{i_id}", name="get_assistant")
def get_assistant(i_id, request: Request):
    from apps.assistants.models import Assistant
    from config.asgi import check_api_key

    ux, e = check_api_key(request)
    if e:
        return e

    ##############################
    # PERMISSION CHECK FOR - LIST_ASSISTANTS
    if not UserPermissionManager.is_authorized(
        user=ux,
        operation=PermissionNames.LIST_ASSISTANTS
    ):
        return raise_not_authorized_error(request)
    ##############################

    try:
        assistant = Assistant.objects.get(
            id=i_id,
            organization__users__in=[ux]
        )

    except Exception as e:
        return JSONResponse(
            {
                "status": statuses.ERROR,
                "message": "An error occurred while fetching the assistant.",
                "errors": {
                    "message": str(e)
                },
                "meta": {
                    "request": request.url.path,
                    "method": request.method,
                    "status_code": 500
                }
            }
        )

    return JSONResponse(
        {
            "status": statuses.SUCCESS,
            "message": "Assistant fetched successfully.",
            "errors": {},
            "data": json.loads(
                serialize(
                    "json",
                    [
                        assistant
                    ]
                )
            ),
            "meta": {
                "request": request.url.path,
                "method": request.method,
                "status_code": 200
            }
        }
    )


######################################################################################################################
# DELETE
######################################################################################################################

@router.delete("/{i_id}", name="delete_assistant")
def delete_assistant(i_id, request: Request):
    from apps.assistants.models import Assistant
    from config.asgi import check_api_key

    ux, e = check_api_key(request)
    if e:
        return e

    ##############################
    # PERMISSION CHECK FOR - DELETE_ASSISTANTS
    if not UserPermissionManager.is_authorized(
        user=ux,
        operation=PermissionNames.DELETE_ASSISTANTS
    ):
        return raise_not_authorized_error(request)
    ##############################

    try:
        obj = Assistant.objects.get(
            id=i_id,
            organization__users__in=[ux]
        )
        obj.delete()

    except Exception as e:
        return JSONResponse(
            {
                "status": statuses.ERROR,
                "message": "An error occurred while fetching the assistant.",
                "errors": {
                    "message": str(e)
                },
                "meta": {
                    "request": request.url.path,
                    "method": request.method,
                    "status_code": 500
                }
            }
        )

    return JSONResponse(
        {
            "status": statuses.SUCCESS,
            "message": "Assistant deleted successfully.",
            "errors": {},
            "meta": {
                "request": request.url.path,
                "method": request.method,
                "status_code": 200
            }
        }
    )
