#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: function_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:43
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

import wonderwords
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.multimodal_chat.utils import (
    BIMOD_STREAMING_END_TAG,
    BIMOD_PROCESS_END,
    BIMOD_NO_TAG_PLACEHOLDER
)

import warnings

from apps.orchestrations.models import (
    OrchestrationQuery
)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")

logger = logging.getLogger(__name__)


class TransmitWebsocketLogSenderType:
    ASSISTANT = "Assistant"
    LEANMOD = "LeanMod"
    ORCHESTRATION = "Orchestrator"
    VOIDFORGER = "VoidForger"

    @staticmethod
    def as_list():
        return [
            TransmitWebsocketLogSenderType.ASSISTANT,
            TransmitWebsocketLogSenderType.LEANMOD,
            TransmitWebsocketLogSenderType.ORCHESTRATION,
            TransmitWebsocketLogSenderType.VOIDFORGER
        ]


def transmit_websocket_log(
    log_message,
    chat_id,
    sender_type,
    stop_tag=BIMOD_STREAMING_END_TAG,
    fermion__is_fermion_supervised=False,
    fermion__export_type=None,
    fermion__endpoint=None
):
    channel_layer = get_channel_layer()

    generic_group_name = None

    if sender_type == TransmitWebsocketLogSenderType.ASSISTANT:
        group_name = f'logs_{chat_id}'

    elif sender_type == TransmitWebsocketLogSenderType.LEANMOD:
        group_name = f'leanmod_logs_{chat_id}'

    elif sender_type == TransmitWebsocketLogSenderType.ORCHESTRATION:

        chat: OrchestrationQuery = OrchestrationQuery.objects.get(
            id=chat_id
        )

        maestro_id = chat.maestro.id

        group_name = f'orchestration_logs_{chat_id}'
        generic_group_name = f'orchestration_generic_logs_{maestro_id}'

    elif sender_type == TransmitWebsocketLogSenderType.VOIDFORGER:
        group_name = f'voidforger_logs_{chat_id}'

    else:
        logger.error(f"Invalid sender type: {sender_type}")
        return

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_log',
            'message': log_message
        }
    )

    if generic_group_name is not None and sender_type == TransmitWebsocketLogSenderType.ORCHESTRATION:

        async_to_sync(channel_layer.group_send)(
            generic_group_name,
            {
                'type': 'send_log',
                'message': log_message
            }
        )

    if stop_tag == BIMOD_STREAMING_END_TAG:

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_log',
                'message': BIMOD_STREAMING_END_TAG
            }
        )

        if generic_group_name is not None and sender_type == TransmitWebsocketLogSenderType.ORCHESTRATION:
            async_to_sync(channel_layer.group_send)(
                generic_group_name,
                {
                    'type': 'send_log',
                    'message': BIMOD_STREAMING_END_TAG
                }
            )

    elif stop_tag == BIMOD_PROCESS_END:

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_log',
                'message': BIMOD_PROCESS_END
            }
        )

        if generic_group_name is not None and sender_type == TransmitWebsocketLogSenderType.ORCHESTRATION:
            async_to_sync(channel_layer.group_send)(
                generic_group_name,
                {
                    'type': 'send_log',
                    'message': BIMOD_PROCESS_END
                }
            )

    else:

        if stop_tag is None or stop_tag == "" or stop_tag == BIMOD_NO_TAG_PLACEHOLDER:
            logger.info("No stop tag provided.")

            pass

        else:
            logger.info("Sending stop tag.")

            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_log',
                    'message': stop_tag
                }
            )

            if generic_group_name is not None and sender_type == TransmitWebsocketLogSenderType.ORCHESTRATION:
                async_to_sync(channel_layer.group_send)(
                    generic_group_name,
                    {
                        'type': 'send_log',
                        'message': stop_tag
                    }
                )

    ######################################################################
    # FERMION MOBILE COPILOT: Check if interaction is Fermion supervised.
    ######################################################################

    if fermion__is_fermion_supervised is True:

        fermion_group_name = f'logs_{fermion__export_type}'

        async_to_sync(channel_layer.group_send)(
            fermion_group_name,
            {
                'type': 'send_log',
                'message': log_message
            }
        )

        if stop_tag == BIMOD_STREAMING_END_TAG:

            async_to_sync(channel_layer.group_send)(
                fermion_group_name,
                {
                    'type': 'send_log',
                    'message': BIMOD_STREAMING_END_TAG
                }
            )

        elif stop_tag == BIMOD_PROCESS_END:

            async_to_sync(channel_layer.group_send)(
                fermion_group_name,
                {
                    'type': 'send_log',
                    'message': BIMOD_PROCESS_END
                }
            )

        else:

            if stop_tag is None or stop_tag == "" or stop_tag == BIMOD_NO_TAG_PLACEHOLDER:

                logger.info("No stop tag provided.")
                pass

            else:
                logger.info("Sending stop tag.")
                async_to_sync(channel_layer.group_send)(
                    fermion_group_name, {
                        'type': 'send_log',
                        'message': stop_tag
                    }
                )

    else:
        logger.info("Interaction is not Fermion supervised, standard web socket communication rules are attempted.")
        pass



def generate_chat_name():
    logger.info("Generating chat name.")

    chat_name_1 = wonderwords.RandomWord().word(word_max_length=8, include_categories=["verb"])
    chat_name_2 = wonderwords.RandomWord().word(word_max_length=8, include_categories=["adjective"])
    chat_name_3 = wonderwords.RandomWord().word(word_max_length=8, include_categories=["noun"])

    chat_name_1 = chat_name_1.capitalize()
    chat_name_2 = chat_name_2.capitalize()
    chat_name_3 = chat_name_3.capitalize()

    return " ".join([chat_name_1, chat_name_2, chat_name_3])
