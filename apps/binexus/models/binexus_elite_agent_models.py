#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_elite_agent_models.py
#  Last Modified: 2024-10-22 18:13:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:13:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


from django.db import models


class BinexusEliteAgent(models.Model):
    binexus_process = models.ForeignKey(
        'binexus.BinexusProcess',
        on_delete=models.CASCADE
    )
    agent_nickname = models.CharField(max_length=255)
    agent_prompt = models.TextField(null=True, blank=True)
    agent_temperature = models.FloatField(default=0.0)
    binexus_fitness_score = models.IntegerField(default=0)
    agent_chromosome_parameters = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent_nickname + " - " + self.binexus_process.process_name + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = 'Binexus Elite Agent'
        verbose_name_plural = 'Binexus Elite Agents'
        ordering = ['-binexus_fitness_score']
        indexes = [
            models.Index(
                fields=['binexus_fitness_score'],
                name='binexus_fitness_score_idx'
            ),
            models.Index(
                fields=['created_at'],
                name='created_at_idx'
            ),
            models.Index(
                fields=['updated_at'],
                name='updated_at_idx'
            ),
            models.Index(fields=[
                'binexus_process'],
                name='binexus_process_idx'
            ),
            models.Index(
                fields=['agent_nickname'],
                name='agent_nickname_idx'
            ),
            models.Index(
                fields=['agent_temperature'],
                name='agent_temperature_idx'
            ),
            models.Index(
                fields=[
                    'created_at',
                    'updated_at'
                ],
                name='created_at_updated_at_idx'
            ),
        ]
