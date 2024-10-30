#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: get_metatempo_connection_config_views.py
#  Last Modified: 2024-10-28 22:26:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 22:26:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.metatempo.models import MetaTempoConnection


@method_decorator(csrf_exempt, name='dispatch')
class MetaTempoView_GetConnectionConfig(View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        api_key = request.POST.get('api_key')
        if not api_key:
            return JsonResponse({"success": False, "error": "API key is required."}, status=400)

        if "Bearer" in api_key:
            api_key = api_key.replace("Bearer", "").strip()

        try:
            connection = MetaTempoConnection.objects.get(connection_api_key=api_key)
        except MetaTempoConnection.DoesNotExist:
            return JsonResponse({"success": False, "error": "Connection not found."}, status=404)

        connection_data = {
            "board": connection.board.title,
            "is_tracking_active": connection.is_tracking_active,
            "optional_context_instructions": connection.optional_context_instructions or "",
            "overall_log_intervals": connection.overall_log_intervals,
            "member_log_intervals": connection.member_log_intervals,
            "tracked_weekdays": connection.tracked_weekdays if connection.tracked_weekdays else [],
            "tracking_start_time": connection.tracking_start_time.strftime(
                '%H:%M') if connection.tracking_start_time else None,
            "tracking_end_time": connection.tracking_end_time.strftime(
                '%H:%M') if connection.tracking_end_time else None,
            "connection_api_key": connection.connection_api_key,
            "created_by_user": connection.created_by_user.username if connection.created_by_user else None,
            "created_at": connection.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": connection.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return JsonResponse({"success": True, "data": connection_data}, status=200)
