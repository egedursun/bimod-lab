#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_node_models.py
#  Last Modified: 2024-10-17 21:48:04
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 21:48:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import secrets
import uuid

from django.db import models

from apps.hadron_prime.utils import HADRON_NODE_AUTHENTICATION_KEY_TOKEN_SIZE


class HadronNode(models.Model):
    system = models.ForeignKey('hadron_prime.HadronSystem', on_delete=models.CASCADE)
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.SET_NULL, null=True, blank=True)
    node_name = models.CharField(max_length=4000)
    node_description = models.TextField()
    optional_instructions = models.TextField(null=True, blank=True)

    # RETRIEVING CURRENT STATE
    current_state_curl = models.CharField(null=True, blank=True)
    current_state_input_params_description = models.TextField(null=True, blank=True)
    current_state_output_params_description = models.TextField(null=True, blank=True)

    # RETRIEVING THE GOAL STATE
    goal_state_curl = models.CharField(null=True, blank=True)
    goal_state_input_params_description = models.TextField(null=True, blank=True)
    goal_state_output_params_description = models.TextField(null=True, blank=True)

    # RETRIEVING THE ERROR CALCULATION
    error_calculation_curl = models.CharField(null=True, blank=True)
    error_calculation_input_params_description = models.TextField(null=True, blank=True)
    error_calculation_output_params_description = models.TextField(null=True, blank=True)

    # RETRIEVING THE SENSORY MEASUREMENTS
    measurements_curl = models.CharField(null=True, blank=True)
    measurements_input_params_description = models.TextField(null=True, blank=True)
    measurements_output_params_description = models.TextField(null=True, blank=True)

    # RETRIEVING THE ACTION SET
    action_set_curl = models.CharField(null=True, blank=True)
    action_set_input_params_description = models.TextField(null=True, blank=True)
    action_set_output_params_description = models.TextField(null=True, blank=True)

    # RETRIEVING THE ANALYTIC CALCULATION RESULTS (IF THERE IS ANY)
    analytic_calculation_curl = models.CharField(null=True, blank=True)
    analytic_calculation_input_params_description = models.TextField(null=True, blank=True)
    analytic_calculation_output_params_description = models.TextField(null=True, blank=True)

    # SENDING REQUEST FOR ACTUATION
    actuation_curl = models.CharField(null=True, blank=True)
    actuation_input_params_description = models.TextField(null=True, blank=True)
    actuation_output_params_description = models.TextField(null=True, blank=True)

    # CONNECTIONS
    subscribed_topics = models.ManyToManyField('hadron_prime.HadronTopic', blank=True)
    state_action_state_history_logs = models.ManyToManyField('hadron_prime.HadronStateErrorActionStateErrorLog',
                                                             blank=True)
    state_action_state_lookback_memory_size = models.IntegerField(default=20)
    publishing_history_logs = models.ManyToManyField('hadron_prime.HadronTopicMessage', blank=True)
    publishing_history_lookback_memory_size = models.IntegerField(default=20)
    topic_messages_history_lookback_memory_size = models.IntegerField(default=50)
    expert_networks = models.ManyToManyField('leanmod.ExpertNetwork', blank=True)
    execution_logs = models.ManyToManyField('hadron_prime.HadronNodeExecutionLog', blank=True)
    speech_logs = models.ManyToManyField('hadron_prime.HadronNodeSpeechLog', blank=True)

    # ACTIVATION TRIGGER FOR THE NODE
    activation_trigger_hashed_param = models.CharField(max_length=1000, null=True, blank=True)
    activation_trigger_authentication_key = models.CharField(max_length=1000, null=True, blank=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.node_name + ' - ' + self.system.system_name + ' - ' + self.system.organization.name

    class Meta:
        verbose_name = 'Hadron Node'
        verbose_name_plural = 'Hadron Nodes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['system', 'node_name']),
            models.Index(fields=['system', 'created_by_user']),
            models.Index(fields=['system', 'created_at']),
            models.Index(fields=['system', 'updated_at']),
        ]

    def save(self, *args, **kwargs):
        super(HadronNode, self).save(*args, **kwargs)
        if self.activation_trigger_hashed_param is None:
            self.activation_trigger_hashed_param = uuid.uuid4().hex + uuid.uuid4().hex
            self.save()
        if self.activation_trigger_authentication_key is None:
            self.activation_trigger_authentication_key = str(secrets.token_urlsafe(HADRON_NODE_AUTHENTICATION_KEY_TOKEN_SIZE))
            self.save()
