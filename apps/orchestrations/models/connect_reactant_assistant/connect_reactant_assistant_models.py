#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connect_reactant_assistant_models.py
#  Last Modified: 2024-11-13 04:32:24
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-13 04:32:25
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


class OrchestrationReactantAssistantConnection(models.Model):
    orchestration_maestro = models.ForeignKey(
        "orchestrations.Maestro",
        on_delete=models.CASCADE
    )

    assistant = models.ForeignKey(
        "assistants.Assistant",
        on_delete=models.CASCADE
    )

    created_by_user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.assistant} - {self.orchestration_maestro}"

    class Meta:
        unique_together = [
            [
                "orchestration_maestro",
                "assistant"
            ],
        ]

        verbose_name = "Orchestration Reactant Assistant Connection"
        verbose_name_plural = "Orchestration Reactant Assistant Connections"

        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=[
                "orchestration_maestro",
                "assistant"
            ]),
            models.Index(fields=[
                "assistant",
                "orchestration_maestro"
            ]),
        ]
