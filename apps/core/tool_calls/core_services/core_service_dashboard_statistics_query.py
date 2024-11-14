#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: core_service_dashboard_statistics_query.py
#  Last Modified: 2024-11-13 05:10:01
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 05:10:59
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from django.contrib.auth.models import User

from apps.dashboard.utils import TransactionStatisticsManager
from apps.llm_core.models import LLMCore

logger = logging.getLogger(__name__)


def run_query_dashboard_statistics(llm_core: LLMCore, user_id: int):
    user = User.objects.get(id=user_id)
    try:
        from apps.core.generative_ai.generative_ai_decode_manager import GenerativeAIDecodeController
        manager = TransactionStatisticsManager(user=user)
        data_statistics = manager.statistics
        output = GenerativeAIDecodeController.provide_analysis(llm_model=llm_core, statistics=data_statistics)
    except Exception as e:
        logger.error(f"Error occurred while running the dashboard statistics query: {e}")
        error = f"There has been an unexpected error on running the dashboard statistics query: {e}"
        return error
    return output
