#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-17 22:28:28
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:28:29
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from apps.hadron_prime.models import HadronNode


class NodeExecutionProcessLogTexts:

    @staticmethod
    def system_initialized(node: HadronNode):
        return f"Hadron System: {node.system.system_name} execution environment is initialized.\n"

    @staticmethod
    def topics_initialized(node: HadronNode):
        return f"Hadron System: {node.subscribed_topics.count()} topics are initialized.\n"

    @staticmethod
    def node_initialized(node: HadronNode):
        return f"Hadron Node: {node.node_name} is initialized.\n"

    @staticmethod
    def memory_initialized(node: HadronNode):
        return f"Hadron Node: {node.node_name} lookback memories are initialized.\n"

    @staticmethod
    def process_started(timestamp):
        return f"Hadron Node execution process started at {timestamp}.\n"

    #####

    @staticmethod
    def state_retrieval_started(timestamp):
        return f"Hadron Node state retrieval process started at {timestamp}.\n"

    @staticmethod
    def state_retrieval_failed(timestamp):
        return f"Hadron Node state retrieval process failed at {timestamp}.\n"

    @staticmethod
    def state_retrieval_completed(timestamp):
        return f"Hadron Node state retrieval process completed at {timestamp}.\n"

    #####

    @staticmethod
    def measurement_retrieval_started(timestamp):
        return f"Hadron Node measurement retrieval process started at {timestamp}.\n"

    @staticmethod
    def measurement_retrieval_failed(timestamp):
        return f"Hadron Node measurement retrieval process failed at {timestamp}.\n"

    @staticmethod
    def measurement_retrieval_completed(timestamp):
        return f"Hadron Node measurement retrieval process completed at {timestamp}.\n"

    #####

    @staticmethod
    def topic_message_processing_started(timestamp):
        return f"Hadron Node topic message processing process started at {timestamp}.\n"

    @staticmethod
    def topic_message_processing_failed(timestamp):
        return f"Hadron Node topic message processing process failed at {timestamp}.\n"

    @staticmethod
    def topic_message_processing_completed(timestamp):
        return f"Hadron Node topic message processing process completed at {timestamp}.\n"

    #####

    @staticmethod
    def node_SEASE_history_retrieval_started(timestamp):
        return f"Hadron Node SEASE history retrieval process started at {timestamp}.\n"

    @staticmethod
    def node_SEASE_history_retrieval_failed(timestamp):
        return f"Hadron Node SEASE history retrieval process failed at {timestamp}.\n"

    @staticmethod
    def node_SEASE_history_retrieval_completed(timestamp):
        return f"Hadron Node SEASE history retrieval process completed at {timestamp}.\n"

    #####

    @staticmethod
    def node_publishing_history_logs_retrieval_started(timestamp):
        return f"Hadron Node publishing history logs retrieval process started at {timestamp}.\n"

    @staticmethod
    def node_publishing_history_logs_retrieval_failed(timestamp):
        return f"Hadron Node publishing history logs retrieval process failed at {timestamp}.\n"

    @staticmethod
    def node_publishing_history_logs_retrieval_completed(timestamp):
        return f"Hadron Node publishing history logs retrieval process completed at {timestamp}.\n"

    #####

    @staticmethod
    def error_calculation_process_started(timestamp):
        return f"Hadron Node error calculation process started at {timestamp}.\n"

    @staticmethod
    def error_calculation_process_failed(timestamp):
        return f"Hadron Node error calculation process failed at {timestamp}.\n"

    @staticmethod
    def error_calculation_process_completed(timestamp):
        return f"Hadron Node error calculation process completed at {timestamp}.\n"

    #####

    @staticmethod
    def analytical_calculation_calls_started(timestamp):
        return f"Hadron Node analytical calculation calls started at {timestamp}.\n"

    @staticmethod
    def analytical_calculation_calls_failed(timestamp):
        return f"Hadron Node analytical calculation calls failed at {timestamp}.\n"

    @staticmethod
    def analytical_calculation_calls_completed(timestamp):
        return f"Hadron Node analytical calculation calls completed at {timestamp}.\n"

    ######

    @staticmethod
    def processing_and_action_determination_layer_started(timestamp):
        return f"Hadron Node processing and action determination layer started at {timestamp}.\n"

    @staticmethod
    def processing_and_action_determination_layer_failed(timestamp):
        return f"Hadron Node processing and action determination layer failed at {timestamp}.\n"

    @staticmethod
    def processing_and_action_determination_layer_completed(timestamp):
        return f"Hadron Node processing and action determination layer completed at {timestamp}.\n"

    ######

    @staticmethod
    def actuation_call_layer_started(timestamp):
        return f"Hadron Node actuation call layer started at {timestamp}.\n"

    @staticmethod
    def actuation_call_layer_failed(timestamp):
        return f"Hadron Node actuation call layer failed at {timestamp}.\n"

    @staticmethod
    def actuation_call_layer_completed(timestamp):
        return f"Hadron Node actuation call layer completed at {timestamp}.\n"

    #####

    @staticmethod
    def post_action_state_evaluation_started(timestamp):
        return f"Hadron Node post-action state evaluation process started at {timestamp}.\n"

    @staticmethod
    def post_action_state_evaluation_failed(timestamp):
        return f"Hadron Node post-action state evaluation process failed at {timestamp}.\n"

    @staticmethod
    def post_action_state_evaluation_completed(timestamp):
        return f"Hadron Node post-action state evaluation process completed at {timestamp}.\n"

    #####

    @staticmethod
    def post_action_error_evaluation_started(timestamp):
        return f"Hadron Node post-action error evaluation process started at {timestamp}.\n"

    @staticmethod
    def post_action_error_evaluation_failed(timestamp):
        return f"Hadron Node post-action error evaluation process failed at {timestamp}.\n"

    @staticmethod
    def post_action_error_evaluation_completed(timestamp):
        return f"Hadron Node post-action error evaluation process completed at {timestamp}.\n"

    #####

    @staticmethod
    def process_completed(timestamp):
        return f"Hadron Node execution process completed successfully at {timestamp}.\n"

    @staticmethod
    def process_failed(error_log: str):
        return f"Hadron Node execution process failed with the following error: {error_log}\n"


HADRON_TOPIC_CATEGORIES = [
    ('alerts', 'Alerts'),
    ('info', 'Info'),
    ('measurements', 'Measurements'),
    ('states', 'States'),
    ('actions', 'Actions'),
    ('commands', 'Commands'),
]


class HadronTopicCategoriesNames:
    ALERTS = 'alerts'  #
    INFO = 'info'  #
    STATES = 'states'  #
    MEASUREMENTS = 'measurements'  #
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


class CURLHttpOptions:
    class StartsWith:
        URL = 'http'
        HEADER = '-H'
        DATA = '-d'
        REQUEST = '-X'

        @staticmethod
        def as_list():
            return [
                CURLHttpOptions.StartsWith.URL,
                CURLHttpOptions.StartsWith.HEADER,
                CURLHttpOptions.StartsWith.DATA,
                CURLHttpOptions.StartsWith.REQUEST
            ]

    class Equals:
        REQUEST = '--request'
        HEADER = '--header'
        DATA = '--data'
        DATA_RAW = '--data-raw'

        @staticmethod
        def as_list():
            return [
                CURLHttpOptions.Equals.REQUEST,
                CURLHttpOptions.Equals.HEADER,
                CURLHttpOptions.Equals.DATA,
                CURLHttpOptions.Equals.DATA_RAW
            ]


class CURLHttpMethods:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'

    @staticmethod
    def as_list():
        return [
            CURLHttpMethods.GET,
            CURLHttpMethods.POST,
            CURLHttpMethods.PUT,
            CURLHttpMethods.PATCH,
            CURLHttpMethods.DELETE
        ]


HADRON_PRIME_TOOL_CALL_MAXIMUM_ATTEMPTS = 3

SPEECH_LOGS_MAXIMUM_LOOKBACK = 10
EXECUTION_LOGS_MAXIMUM_LOOKBACK = 10
