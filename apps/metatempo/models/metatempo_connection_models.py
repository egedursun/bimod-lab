#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: metatempo_board_models.py
#  Last Modified: 2024-10-28 19:40:45
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:40:45
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

from apps.metatempo.utils import (
    METATEMPO_OVERALL_LOG_INTERVALS,
    MetaTempoOverallLogIntervalsNames,
    METATEMPO_MEMBER_LOG_INTERVALS,
    MetaTempoMemberLogIntervalsNames
)


class MetaTempoConnection(models.Model):
    board = models.OneToOneField(
        'metakanban.MetaKanbanBoard',
        on_delete=models.CASCADE,
        unique=True
    )

    is_tracking_active = models.BooleanField(default=True)

    optional_context_instructions = models.TextField(blank=True, null=True)

    overall_log_intervals = models.CharField(
        max_length=1000,
        choices=METATEMPO_OVERALL_LOG_INTERVALS,
        default=MetaTempoOverallLogIntervalsNames.DAILY
    )

    member_log_intervals = models.CharField(
        max_length=1000,
        choices=METATEMPO_MEMBER_LOG_INTERVALS,
        default=MetaTempoMemberLogIntervalsNames.TIMES_6_PER_HOUR
    )

    tracked_weekdays = models.JSONField(blank=True, null=True)
    tracking_start_time = models.TimeField(blank=True, null=True)
    tracking_end_time = models.TimeField(blank=True, null=True)

    connection_api_key = models.CharField(
        max_length=1000,
        blank=True,
        null=True
    )

    created_by_user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='metatempo_board_connections_created',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.board} - {self.is_tracking_active}'

    class Meta:
        verbose_name = 'MetaTempo Board Connection'
        verbose_name_plural = 'MetaTempo Board Connections'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=[
                'board', 'is_tracking_active'
            ]),
            models.Index(fields=[
                'connection_api_key'
            ]),
            models.Index(fields=[
                'created_by_user'
            ]),
            models.Index(fields=[
                'created_at'
            ]),
            models.Index(fields=[
                'updated_at'
            ]),
        ]
