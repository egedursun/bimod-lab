#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_screenshot_delivery_views.py
#  Last Modified: 2024-10-28 20:39:27
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 20:39:28
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
import logging

from django.contrib.auth.models import (
    User
)

from django.http import JsonResponse

from django.utils.decorators import (
    method_decorator
)

from django.views import View

from django.views.decorators.csrf import (
    csrf_exempt
)

from apps.core.generative_ai.utils import (
    GPT_DEFAULT_ENCODING_ENGINE,
    ChatRoles
)

from apps.core.internal_cost_manager.costs_map import (
    InternalServiceCosts
)

from apps.core.metatempo.metatempo_execution_handler import (
    MetaTempoExecutionManager
)

from apps.llm_transaction.models import (
    LLMTransaction
)

from apps.llm_transaction.utils import (
    LLMTransactionSourcesTypesNames,
    LLMTokenTypesNames
)

from apps.metatempo.models import (
    MetaTempoConnection,
    MetaTempoMemberLog
)

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class MetaTempoView_ScreenshotDelivery(View):
    def get(
        self,
        request,
        *args,
        **kwargs
    ):
        return self.post(
            request,
            *args,
            **kwargs
        )

    def post(self, request, *args, **kwargs):
        metatempo_user_auth_key = request.POST.get('metatempo_user_auth_key')
        metatempo_api_key = request.POST.get('metatempo_api_key')

        screenshot_image_png = request.FILES.get('screenshot_image_png')
        snapshot_metadata = request.POST.get('snapshot_metadata')

        if not metatempo_user_auth_key:
            logger.error("[metatempo_screenshot_delivery] metatempo_user_auth_key is required.")

            return JsonResponse(
                {
                    "success": False,
                    "error": "metatempo_user_auth_key is required."
                },
                status=400
            )

        if not metatempo_api_key:
            logger.error("[metatempo_screenshot_delivery] metatempo_api_key is required.")

            return JsonResponse(
                {
                    "success": False,
                    "error": "metatempo_api_key is required."
                },
                status=400
            )

        if not screenshot_image_png:
            logger.error("[metatempo_screenshot_delivery] screenshot_image_png is required.")

            return JsonResponse(
                {
                    "success": False,
                    "error": "screenshot_image_png is required."
                },
                status=400
            )

        if not snapshot_metadata:
            logger.error("[metatempo_screenshot_delivery] snapshot_metadata is required.")

            return JsonResponse(
                {
                    "success": False,
                    "error": "snapshot_metadata is required."
                },
                status=400
            )

        try:
            context_user = User.objects.filter(
                profile__metatempo_tracking_auth_key=metatempo_user_auth_key
            ).first()

            if not context_user:
                logger.error("[metatempo_screenshot_delivery] User not found.")

                return JsonResponse(
                    {
                        "success": False,
                        "error": "User not found."
                    },
                    status=404
                )

        except Exception as e:
            logger.error(f"[metatempo_screenshot_delivery] Error processing user auth key: {str(e)}")

            return JsonResponse(
                {
                    "success": False,
                    "error": str(e)
                },
                status=500
            )

        try:
            if "Bearer" in metatempo_api_key:
                metatempo_api_key = metatempo_api_key.replace(
                    "Bearer",
                    ""
                ).strip()

        except Exception as e:
            logger.error(f"[metatempo_screenshot_delivery] Error processing API key: {str(e)}")

            return JsonResponse(
                {
                    "success": False,
                    "error": str(e)
                },
                status=500
            )

        try:
            if "Bearer" in metatempo_user_auth_key:
                metatempo_user_auth_key = metatempo_user_auth_key.replace(
                    "Bearer",
                    ""
                ).strip()

        except Exception as e:
            logger.error(f"[metatempo_screenshot_delivery] Error processing user auth key: {str(e)}")

            return JsonResponse(
                {
                    "success": False,
                    "error": str(e)
                },
                status=500
            )

        connection: MetaTempoConnection = MetaTempoConnection.objects.filter(
            connection_api_key=metatempo_api_key
        ).first()

        if not connection:
            logger.error("[metatempo_screenshot_delivery] Connection not found.")

            return JsonResponse(
                {
                    "success": False,
                    "error": "Connection not found."
                },
                status=404
            )

        if connection.connection_api_key != metatempo_api_key:
            logger.error("[metatempo_screenshot_delivery] Invalid API Key.")

            return JsonResponse(
                {
                    "success": False,
                    "error": "Invalid API Key."
                },
                status=401
            )

        if connection.is_tracking_active is False:
            logger.error("[metatempo_screenshot_delivery] Tracking is not active for this board.")

            return JsonResponse(
                {
                    "success": False,
                    "error": "Tracking is not active for this board."
                },
                status=403
            )

        try:
            snapshot_metadata = json.loads(
                snapshot_metadata
            )

            if 'timestamp' not in snapshot_metadata:
                logger.error("[metatempo_screenshot_delivery] timestamp is required in snapshot metadata.")

                return JsonResponse(
                    {
                        "success": False,
                        "error": "timestamp is required in snapshot metadata."},
                    status=400
                )

            if 'identifier_uuid' not in snapshot_metadata:
                logger.error("[metatempo_screenshot_delivery] identifier_uuid is required in snapshot metadata.")

                return JsonResponse(
                    {
                        "success": False,
                        "error": "identifier_uuid is required in snapshot metadata."
                    },
                    status=400
                )

        except Exception as e:
            logger.error(f"[metatempo_screenshot_delivery] Error processing snapshot metadata: {str(e)}")

            snapshot_metadata = {}

        identifier_uuid = snapshot_metadata.get('identifier_uuid')
        try:
            exists = MetaTempoMemberLog.objects.filter(
                identifier_uuid=identifier_uuid
            )

            if exists:
                logger.error("[metatempo_screenshot_delivery] This record has already been saved.")

                return JsonResponse(
                    {
                        "success": True,
                        "error": "This record has already been saved."
                    },
                    status=200
                )

        except Exception as e:
            logger.error(f"[metatempo_screenshot_delivery] Error processing identifier_uuid: {str(e)}")

            return JsonResponse(
                {
                    "success": False,
                    "error": str(e)
                },
                status=500
            )

        try:
            xc = MetaTempoExecutionManager(
                metatempo_connection_id=connection.id
            )

            result, error = xc.interpret_and_save_log_snapshot(
                snapshot_metadata=snapshot_metadata,
                log_screenshot_data=screenshot_image_png.read(),
                context_user=context_user
            )

            if error:
                logger.error(f"[metatempo_screenshot_delivery] Error processing screenshot: {error}")

                return JsonResponse(
                    {
                        "success": False,
                        "error": error
                    },
                    status=500
                )

        except Exception as e:
            logger.error(f"[metatempo_screenshot_delivery] Exception occurred: {str(e)}")

            return JsonResponse(
                {
                    "success": False,
                    "error": str(e)
                },
                status=500
            )

        try:
            tx = LLMTransaction(
                organization=connection.board.project.organization,
                model=connection.board.llm_model,
                responsible_user=connection.board.created_by_user,
                responsible_assistant=None,
                encoding_engine=GPT_DEFAULT_ENCODING_ENGINE,
                transaction_type=ChatRoles.SYSTEM,
                transaction_source=LLMTransactionSourcesTypesNames.METATEMPO,
                is_tool_cost=True,
                llm_token_type=LLMTokenTypesNames.OUTPUT,
            )

            tx.save()

            logger.info(f"[metatempo_screenshot_delivery] Created LLMTransaction for MetaTempo Screenshot Log.")

        except Exception as e:
            logger.error(
                f"[metatempo_screenshot_delivery] Error creating LLMTransaction for Screenshot Log. Error: {e}")
            pass

        return JsonResponse(
            {
                "success": True,
                "error": None
            },
            status=200
        )
