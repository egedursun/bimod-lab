#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: binexus_process_models.py
#  Last Modified: 2024-10-22 18:04:50
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-22 18:04:50
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


class BinexusProcess(models.Model):
    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE
    )

    llm_model = models.ForeignKey(
        'llm_core.LLMCore',
        on_delete=models.CASCADE
    )

    process_name = models.CharField(max_length=255)
    process_description = models.TextField()

    process_objective = models.TextField(blank=True, null=True)
    process_success_criteria = models.TextField(blank=True, null=True)

    fitness_manager_selectiveness = models.FloatField(default=0.5)

    additional_genes = models.JSONField(
        default=dict,
        blank=True,
        null=True
    )

    # Optimization Hyper-Parameters
    optimization_generations = models.IntegerField(default=10)
    optimization_population_size = models.IntegerField(default=5)
    optimization_breeding_pool_rate = models.FloatField(default=0.4)

    optimization_mutation_rate_per_individual = models.FloatField(default=0.1)
    optimization_mutation_rate_per_gene = models.FloatField(default=0.1)
    optimization_crossover_rate = models.FloatField(default=0.5)
    self_breeding_possible = models.BooleanField(default=True)

    # Post-Processing History Logs
    post_processing_history_average_fitness_per_epoch = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    post_processing_history_best_fitness_per_epoch = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    post_processing_history_worst_fitness_per_epoch = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    post_processing_history_average_of_average_fitnesses = models.FloatField(
        default=0.0,
        blank=True,
        null=True
    )

    post_processing_history_average_of_best_fitnesses = models.FloatField(
        default=0.0,
        blank=True,
        null=True
    )

    post_processing_history_average_of_worst_fitnesses = models.FloatField(
        default=0.0,
        blank=True,
        null=True
    )

    post_processing_history_visual_chart = models.ImageField(
        upload_to='binexus_process_visual_charts/%Y/%m/%d/',
        blank=True,
        null=True
    )

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.process_name + " - " + self.organization.name + " - " + self.llm_model.nickname + " - " + self.created_at.strftime(
            "%Y-%m-%d %H:%M:%S")

    class Meta:
        verbose_name = 'Binexus Process'
        verbose_name_plural = 'Binexus Processes'

        ordering = ['-created_at']

        unique_together = [
            [
                "organization",
                "process_name"
            ],
        ]

        indexes = [
            models.Index(
                fields=[
                    'organization'
                ]
            ),
            models.Index(
                fields=[
                    'organization',
                    'llm_model'
                ]
            ),
            models.Index(
                fields=[
                    'organization',
                    'llm_model',
                    'created_by_user'
                ]
            ),
            models.Index(
                fields=[
                    'organization',
                    'llm_model',
                    'created_by_user',
                    'created_at'
                ]
            ),
        ]
