#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: voidforger_models.py
#  Last Modified: 2024-11-15 15:49:37
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-15 21:39:16
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

from django.db import models

from apps.assistants.utils import AGENT_SPEECH_LANGUAGES
from apps.voidforger.utils import VOIDFORGER_RUNTIME_STATUSES, VoidForgerRuntimeStatusesNames

logger = logging.getLogger(__name__)


class VoidForger(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    llm_model = models.ForeignKey('llm_core.LLMCore', on_delete=models.CASCADE, null=True, blank=True)
    organizations = models.ManyToManyField('organization.Organization', blank=True)
    additional_instructions = models.TextField(null=True, blank=True)
    tone = models.CharField(max_length=100, default="Professional and Assertive")
    response_language = models.CharField(max_length=100, choices=AGENT_SPEECH_LANGUAGES, default="auto")

    runtime_status = models.CharField(max_length=100, choices=VOIDFORGER_RUNTIME_STATUSES,
                                      default=VoidForgerRuntimeStatusesNames.PAUSED)
    maximum_actions_per_cycle = models.IntegerField(default=5)
    auto_run_current_cycle = models.IntegerField(default=0)
    auto_run_max_lifetime_cycles = models.IntegerField(default=1_000)
    auto_run_trigger_interval_minutes = models.IntegerField(default=15)
    short_term_memory_max_messages = models.IntegerField(default=25)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_auto_execution_started_at = models.DateTimeField(null=True, blank=True)
    last_auto_execution_ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s VoidForger"

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        from apps.organization.models import Organization
        from apps.llm_core.models import LLMCore

        organizations = Organization.objects.filter(users__in=[self.user])
        if not self.pk:
            available_llms = LLMCore.objects.filter(organization__in=organizations)
            if len(available_llms) > 0:
                self.llm_model = available_llms[0]
            else:
                logger.error(f"No LLM model available for VoidForger, defaulting to no LLM mode")
                self.llm_model = None

        super(VoidForger, self).save(force_insert, force_update, using, update_fields)

        try:
            self.organizations.set(organizations)
        except Exception as e:
            logger.error(f"Error while setting organizations for VoidForger, defaulting to no organization mode: {e}")
            self.organizations.set([])

    class Meta:
        verbose_name = "VoidForger"
        verbose_name_plural = "VoidForgers"
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['user', 'runtime_status']),
            models.Index(fields=['user', 'runtime_status', 'created_at']),
            models.Index(fields=['user', 'runtime_status', 'updated_at']),
            models.Index(fields=['user', 'runtime_status', 'created_at', 'updated_at']),
            models.Index(fields=['user', 'runtime_status', 'created_at', 'updated_at', 'llm_model']),
        ]
