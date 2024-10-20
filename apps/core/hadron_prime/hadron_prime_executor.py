#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_prime_executor.py
#  Last Modified: 2024-10-17 22:28:15
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 22:28:15
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

from django.utils import timezone

from apps.hadron_prime.models import HadronNode, HadronSystem, HadronTopic, HadronNodeExecutionLog, \
    HadronStateErrorActionStateErrorLog, HadronTopicMessage
from apps.hadron_prime.utils import HadronNodeExecutionStatusesNames
from apps.core.hadron_prime.utils import NodeExecutionProcessLogTexts, HadronTopicCategoriesNames
from apps.core.hadron_prime.handlers import (s1_state_evaluation_handlers, s2_measurement_evaluation_handlers,
                                             s3_read_topics_handlers, s4_sease_history_evaluation_handlers,
                                             s5_publishing_history_evaluation_handlers,
                                             s6_calculate_current_error_handlers, s7_analytical_calculation_handlers,
                                             s8_determine_action_with_ai_handlers, s9_perform_actuation_handlers)

logger = logging.getLogger(__name__)


class HadronPrimeExecutor:

    def __init__(self, node: HadronNode, execution_log_object: HadronNodeExecutionLog):
        self.node = node
        self.system: HadronSystem = node.system
        self.topics = self.node.subscribed_topics
        self.execution_log_object = execution_log_object
        self.topic_message_history_memory_size = self.node.topic_messages_history_lookback_memory_size
        self.publish_history_memory_size = self.node.publishing_history_lookback_memory_size
        self.sease_history_memory_size = self.node.state_action_state_lookback_memory_size
        self._update_execution_log_object_status(new_status=HadronNodeExecutionStatusesNames.PENDING,
                                                 log_text=NodeExecutionProcessLogTexts.memory_initialized(
                                                        node=self.node))
        self.expert_nets = self.node.expert_networks.all() if self.node.expert_networks else []

    def _update_execution_log_object_status(self, new_status: str, log_text: str):
        if new_status not in HadronNodeExecutionStatusesNames.as_list():
            raise ValueError('Invalid status detected for execution.')
        try:
            xc_log = self.execution_log_object
            xc_log.execution_status = new_status
            xc_log.execution_log += log_text
            xc_log.save()
        except Exception as e:
            logger.error(f"Error occurred while updating the execution log object status: {e}")
            return False
        logger.info(f"Execution log object status updated to: {new_status}")
        return True

    def _create_sease_log_and_append_to_node_sease_logs(self, sease_log: HadronStateErrorActionStateErrorLog):
        try:
            sease_log.save()
            self.node.state_action_state_history_logs.add(sease_log)
            self.node.save()
        except Exception as e:
            logger.error(f"Error occurred while creating and appending the SEASE log to the node: {e}")
            return False
        logger.info("SEASE log created and appended to the node.")
        return True

    def _create_topic_message_and_append_to_node_publish_history(self, topic_message: HadronTopicMessage):
        try:
            self.node.publishing_history_logs.add(topic_message)
            self.node.save()
        except Exception as e:
            logger.error(f"Error occurred while creating and appending the topic message to the node: {e}")
            return False
        logger.info("Topic message created and appended to the node.")
        return True

    def _publish_message_to_topic(self, event_type: str, message: str):
        if event_type not in HadronTopicCategoriesNames.as_list():
            raise ValueError('Invalid topic category detected for publishing.')

        for topic in self.topics.all():
            topic: HadronTopic
            if topic.topic_category == event_type:
                try:
                    topic_message = HadronTopicMessage(topic=topic, sender_node=self.node, message=message)
                    topic_message.save()
                    self._create_topic_message_and_append_to_node_publish_history(topic_message)
                except Exception as e:
                    logger.error(f"Error occurred while publishing the message to the topic: {e}")
                    return False
        logger.info("Message published to the relevant topic(s) successfully.")
        return True

    def _structure_sease_log(self, old_state, old_error, action, new_state, new_error):
        sease_log = HadronStateErrorActionStateErrorLog.objects.create(
            node=self.node, old_state=old_state, old_error=old_error, action=action, new_state=new_state,
            new_error=new_error)
        return sease_log

    def _retrieve_sease_logs(self):
        return self.node.state_action_state_history_logs.order_by('-created_at')[:self.sease_history_memory_size]

    def _retrieve_publish_history(self):
        return self.node.publishing_history_logs.order_by('-created_at')[:self.publish_history_memory_size]

    #####

    def execute_hadron_node(self):
        success, error = True, None
        self._update_execution_log_object_status(
            new_status=HadronNodeExecutionStatusesNames.RUNNING,
            log_text=NodeExecutionProcessLogTexts.process_started(timestamp=timezone.now())
        )
        try:
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.state_retrieval_started(timestamp=timezone.now())
            )
            current_state_data, goal_state_data, error = s1_state_evaluation_handlers.evaluate_state(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while evaluating the state: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.state_retrieval_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("State retrieved successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.state_retrieval_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to retrieve the current state data successfully.")
            self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.STATES, message=str(current_state_data))

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.measurement_retrieval_started(timestamp=timezone.now())
            )
            measurement_data, error = s2_measurement_evaluation_handlers.evaluate_measurements(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while evaluating the measurements: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.measurement_retrieval_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Measurements evaluated successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.measurement_retrieval_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to retrieve the current sensory measurements data successfully.")
            self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.MEASUREMENTS, message=str(measurement_data))

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.topic_message_processing_started(timestamp=timezone.now())
            )
            structured_topic_messages, error = s3_read_topics_handlers.structure_topic_messages(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while structuring the topic messages: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.topic_message_processing_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Topic messages structured successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.topic_message_processing_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to retrieve and process the topic messages successfully.")

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.node_SEASE_history_retrieval_started(timestamp=timezone.now())
            )
            sease_logs, error = s4_sease_history_evaluation_handlers.retrieve_sease_logs(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while retrieving the SEASE logs: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.node_SEASE_history_retrieval_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("SEASE logs retrieved successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.node_SEASE_history_retrieval_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to retrieve and process the previous SEASE logs successfully.")

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.node_publishing_history_logs_retrieval_started(timestamp=timezone.now())
            )
            publish_history_logs, error = s5_publishing_history_evaluation_handlers.retrieve_publish_history_logs(
                node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while retrieving the publishing history logs: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.node_publishing_history_logs_retrieval_failed(
                        timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Publishing history logs retrieved successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.node_publishing_history_logs_retrieval_completed(
                    timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to retrieve and process my previous publishing history logs successfully.")

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.error_calculation_process_started(timestamp=timezone.now())
            )
            error_measurement, error = s6_calculate_current_error_handlers.calculate_error_data(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while calculating the error data: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.error_calculation_process_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Error calculation process completed successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.error_calculation_process_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to retrieve and process the current error measurement data successfully.")

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.analytical_calculation_calls_started(timestamp=timezone.now())
            )
            analytical_data, error = s7_analytical_calculation_handlers.calculate_analytical_data(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while calculating the analytical data: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.analytical_calculation_calls_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Analytical calculation calls completed successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.analytical_calculation_calls_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to calculate the analytical data as an appendix successfully.")

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.processing_and_action_determination_layer_started(
                    timestamp=timezone.now())
            )
            determined_action, command, error = s8_determine_action_with_ai_handlers.determine_action_with_ai(
                node=self.node, current_state=current_state_data, goal_state=goal_state_data,
                error_calculation=error_measurement, measurements=measurement_data,
                topic_messages=structured_topic_messages, sease_logs=sease_logs,
                publish_history_logs=publish_history_logs, analytical_data=analytical_data)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while determining the action with AI: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.processing_and_action_determination_layer_failed(
                        timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Action determined successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.processing_and_action_determination_layer_completed(
                    timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to determine the next action I will take successfully.")
            self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.COMMANDS, message=command)

            #####

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.actuation_call_layer_started(timestamp=timezone.now())
            )
            success, error = s9_perform_actuation_handlers.perform_actuation(node=self.node, determined_action=determined_action)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while executing the actuation call: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.actuation_call_layer_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Actuation call executed successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.actuation_call_layer_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to perform my actuation call successfully.")
            self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ACTIONS, message=str(determined_action))

            #####

            # POST-ACTION STATE AND ERROR CALCULATION

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.post_action_state_evaluation_started(timestamp=timezone.now())
            )
            new_current_state_data, new_goal_state_data, error = s1_state_evaluation_handlers.evaluate_state(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while evaluating the updated state: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.post_action_state_evaluation_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Updated state evaluated successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.post_action_state_evaluation_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to retrieve the updated state data after my action successfully.")

            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.post_action_error_evaluation_started(timestamp=timezone.now())
            )
            new_error_measurement, error = s6_calculate_current_error_handlers.calculate_error_data(node=self.node)
            if error:
                success, error = False, error
                logger.error(f"Error occurred while calculating the updated error data: {error}")
                self._update_execution_log_object_status(
                    new_status=HadronNodeExecutionStatusesNames.FAILED,
                    log_text=NodeExecutionProcessLogTexts.post_action_error_evaluation_failed(timestamp=timezone.now())
                )
                self._publish_message_to_topic(event_type=HadronTopicCategoriesNames.ALERTS, message=error)
                return success, error
            logger.info("Updated error data calculated successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.RUNNING,
                log_text=NodeExecutionProcessLogTexts.post_action_error_evaluation_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to calculate the updated error measurement data after my action successfully.")

            #####

            sease_log = self._structure_sease_log(
                old_state=current_state_data, old_error=error_measurement, action=determined_action,
                new_state=new_current_state_data, new_error=new_error_measurement)
            self._create_sease_log_and_append_to_node_sease_logs(sease_log)
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to create a new SEASE log after performing my action successfully.")

            #####

            logger.info("Hadron node execution completed successfully.")
            self._update_execution_log_object_status(
                new_status=HadronNodeExecutionStatusesNames.COMPLETED,
                log_text=NodeExecutionProcessLogTexts.process_completed(timestamp=timezone.now())
            )
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.INFO,
                message="I managed to complete my execution process successfully.")

        except Exception as e:
            logger.error(f"Error occurred while executing the Hadron node: {e}")
            self._publish_message_to_topic(
                event_type=HadronTopicCategoriesNames.ALERTS,
                message=f"I have failed to complete the execution process due to the following error: {e}")
            return False, f"Error occurred while executing the Hadron node: {e}"

        logger.info("Hadron node executed successfully.")
        return success, error
