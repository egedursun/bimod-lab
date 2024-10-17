#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-08 21:14:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-08 21:14:31
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

logger = logging.getLogger(__name__)


def get_error_on_context_memory_handling_log(error_log: str):
    logger.error(f"[ChatContextManager.forget_oldest_chat_messages] An error occurred while creating the system prompt "
                    f"for the operation: {str(error_log)}")
    structured_log = f"[ChatContextManager.forget_oldest_chat_messages] An error occurred while creating the "
    f"system prompt for the operation: {str(error_log)}"
    return structured_log


def get_structured_memory_contents(message):
    intra_memory_contents = f"""
        ________________________________________
        i. Chat Role: {message["role"]}
        ii. Context Content:
        '''
        {message["content"]}
        '''
        ________________________________________
    """
    return intra_memory_contents
