#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: hadron_sas_log_models.py
#  Last Modified: 2024-10-17 21:48:31
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-17 21:48:32
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


class HadronStateErrorActionStateErrorLog(models.Model):
    node = models.ForeignKey('hadron_prime.HadronNode', on_delete=models.CASCADE)
    old_state = models.TextField()
    old_error = models.TextField()
    action = models.TextField()
    new_state = models.TextField()
    new_error = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.node.node_name + ' - ' + self.action + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Hadron State-Error-Action-State-Error Log'
        verbose_name_plural = 'Hadron State-Error-Action-State-Error Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['node', 'action']),
            models.Index(fields=['node', 'created_at']),
        ]
