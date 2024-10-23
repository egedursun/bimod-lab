#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: s3_read_topics_handlers.py
#  Last Modified: 2024-10-17 22:31:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:31:05
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

from apps.hadron_prime.models import HadronNode, HadronTopicMessage, HadronTopic


logger = logging.getLogger(__name__)


def structure_topic_messages(node: HadronNode):
    structured_topic_messages, error = "N/A", None
    hadron_topics = node.subscribed_topics.all()

    topic_messages_string = {}
    chunk_size = (node.topic_messages_history_lookback_memory_size // len(hadron_topics))
    logger.info("Starting to structure the topic messages for the node.")
    for topic in hadron_topics:
        topic: HadronTopic
        topic_messages = HadronTopicMessage.objects.filter(topic=topic).order_by('-created_at')[:chunk_size]

        for topic_message in topic_messages:
            topic_message: HadronTopicMessage
            try:
                if topic.topic_name not in topic_messages:
                    topic_messages_string[topic.topic_name] = str(f"[SENDER_NODE_NAME | MESSAGE | CREATED_AT]" + "\n")
                    topic_messages_string[topic.topic_name] = f"[{str(topic_message.sender_node.node_name)} | {str(topic_message.message)} | {str(topic_message.created_at)}]" + "\n"
                else:
                    topic_messages_string[topic.topic_name] += f"[{str(topic_message.sender_node.node_name)} | {str(topic_message.message)} | {str(topic_message.created_at)}]" + "\n"
            except Exception as e:
                error = str(e)
                logger.error(f"Error while structuring the topic messages for the node: {error}")
    logger.info("Finished structuring the topic messages for the node.")

    topic_metadata_string = str(f"[TOPIC_NAME | TOPIC_CATEGORY | TOPIC_DESCRIPTION | TOPIC_PURPOSE | CREATED_AT]" + "\n")
    logger.info("Starting to structure the topic metadata for the node.")
    for topic in hadron_topics:
        topic: HadronTopic
        topic_metadata_string += str(f"[{str(topic.topic_name)} | {str(topic.topic_category)} | {str(topic.topic_description)} | {str(topic.topic_purpose)} | {str(topic.created_at)}]" + "\n")
    logger.info("Finished structuring the topic metadata for the node.")

    structured_topic_messages = f"""
        ### **TOPIC METADATA:**
        '''
        {str(topic_metadata_string)}
        '''

        ### **LAST TOPIC MESSAGES PER TOPIC:**
        '''
        {str(topic_messages_string)}
        '''

        '''
        *Total Number of Last Messages Included: {node.topic_messages_history_lookback_memory_size}*
        '''

        -----
    """
    logger.info("Structured the combined topic messages for the node.")
    return structured_topic_messages, error
