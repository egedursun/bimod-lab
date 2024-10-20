#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-17 21:40:53
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 21:40:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


HADRON_TOPIC_CATEGORIES = [
    ('alerts', 'Alerts'),
    ('info', 'Info'),
    ('states', 'States'),
    ('measurements', 'Measurements'),
    ('actions', 'Actions'),
    ('commands', 'Commands'),
]


class HadronTopicCategoriesNames:
    ALERTS = 'alerts'
    INFO = 'info'
    STATES = 'states'
    MEASUREMENTS = 'measurements'
    ACTIONS = 'actions'
    COMMANDS = 'commands'

    @staticmethod
    def as_list():
        return [
            HadronTopicCategoriesNames.ALERTS,
            HadronTopicCategoriesNames.MEASUREMENTS,
            HadronTopicCategoriesNames.STATES,
            HadronTopicCategoriesNames.ACTIONS,
            HadronTopicCategoriesNames.COMMANDS,
            HadronTopicCategoriesNames.INFO
        ]


HADRON_NODE_ADMIN_LIST = ['node_name', 'system', 'created_by_user', 'created_at', 'updated_at']
HADRON_NODE_ADMIN_FILTER = ['system', 'created_by_user', 'created_at', 'updated_at']
HADRON_NODE_ADMIN_SEARCH = ['node_name', 'system', 'created_by_user']

HADRON_SAS_LOG_ADMIN_LIST = ['node', 'old_state', 'action', 'new_state', 'created_at']
HADRON_SAS_LOG_ADMIN_FILTER = ['node', 'action']
HADRON_SAS_LOG_ADMIN_SEARCH = ['node', 'action']

HADRON_SYSTEM_ADMIN_LIST = ['organization', 'system_name', 'created_by_user', 'created_at', 'updated_at']
HADRON_SYSTEM_ADMIN_FILTER = ['organization', 'created_by_user']
HADRON_SYSTEM_ADMIN_SEARCH = ['system_name', 'system_description']

HADRON_TOPIC_ADMIN_LIST = ['topic_name', 'system', 'topic_category', 'created_by_user', 'created_at']
HADRON_TOPIC_ADMIN_FILTER = ['system', 'created_by_user']
HADRON_TOPIC_ADMIN_SEARCH = ['topic_name', 'system__system_name', 'created_by_user__username']

HADRON_TOPIC_MESSAGE_ADMIN_LIST = ['topic', 'sender_node', 'created_at']
HADRON_TOPIC_MESSAGE_ADMIN_FILTER = ['topic', 'sender_node', 'created_at']
HADRON_TOPIC_MESSAGE_ADMIN_SEARCH = ['topic', 'sender_node', 'created_at']

HADRON_NODE_EXECUTION_LOG_ADMIN_LIST = ('node', 'created_at')
HADRON_NODE_EXECUTION_LOG_ADMIN_FILTER = ('node', 'created_at')
HADRON_NODE_EXECUTION_LOG_ADMIN_SEARCH = ('node', 'created_at')


HADRON_NODE_AUTHENTICATION_KEY_TOKEN_SIZE = 64


HADRON_NODE_EXECUTION_STATUSES = [
    ('DEACTIVE', 'DEACTIVE'),
    ('PENDING', 'PENDING'),
    ('RUNNING', 'RUNNING'),
    ('COMPLETED', 'COMPLETED'),
    ('FAILED', 'FAILED'),
]


class HadronNodeExecutionStatusesNames:
    DEACTIVE = 'DEACTIVE'
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

    @staticmethod
    def as_list():
        return [
            HadronNodeExecutionStatusesNames.DEACTIVE,
            HadronNodeExecutionStatusesNames.PENDING,
            HadronNodeExecutionStatusesNames.RUNNING,
            HadronNodeExecutionStatusesNames.COMPLETED,
            HadronNodeExecutionStatusesNames.FAILED
        ]
