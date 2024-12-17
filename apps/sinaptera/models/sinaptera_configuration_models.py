#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: sinaptera_configuration_models.py
#  Last Modified: 2024-12-14 17:22:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-12-14 17:22:47
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


class SinapteraConfiguration(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='sinaptera_configuration',
        unique=True
    )

    nitro_boost = models.BooleanField(default=False)

    is_active_on_assistants = models.BooleanField(default=False)
    is_active_on_leanmods = models.BooleanField(default=False)
    is_active_on_orchestrators = models.BooleanField(default=False)
    is_active_on_voidforgers = models.BooleanField(default=False)

    rubric_weight_comprehensiveness = models.IntegerField(default=10)
    rubric_weight_accuracy = models.IntegerField(default=9)
    rubric_weight_relevancy = models.IntegerField(default=8)
    rubric_weight_cohesiveness = models.IntegerField(default=8)
    rubric_weight_diligence = models.IntegerField(default=6)
    rubric_weight_grammar = models.IntegerField(default=4)
    rubric_weight_naturalness = models.IntegerField(default=2)

    branching_factor = models.IntegerField(default=4)
    branch_keeping_factor = models.IntegerField(default=2)
    evaluation_depth_factor = models.IntegerField(default=4)

    """
        [
            {
                "name": "Humorousness",
                "weight": 5,  # An integer between 0 and 10
                "score_3x_description: "The response is humorous and engaging, making the user laugh.",
                "score_2x_description: "The response is somewhat humorous and engaging, making the user smile.",
                "score_1x_description: "The response is not humorous or engaging, but it is not boring either.",
                "score_0x_description: "The response is not humorous or engaging, making the user bored.",
            }
        ]
    """

    additional_rubric_criteria = models.JSONField(
        default=list,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sinaptera Configuration for {self.user.username}, created at {self.created_at}"

    class Meta:
        verbose_name = "Sinaptera Configuration"
        verbose_name_plural = "Sinaptera Configurations"

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]
