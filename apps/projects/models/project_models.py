#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: project_models.py
#  Last Modified: 2024-10-24 22:00:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:00:05
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


class ProjectItem(models.Model):
    organization = models.ForeignKey('organization.Organization', on_delete=models.CASCADE)

    project_name = models.TextField()
    project_department = models.TextField()
    project_description = models.TextField()

    project_status = models.CharField(max_length=1000, blank=True, null=True)
    project_priority = models.CharField(max_length=1000, blank=True, null=True)
    project_risk_level = models.CharField(max_length=1000, blank=True, null=True)
    project_goals = models.TextField(blank=True, null=True)
    project_constraints = models.TextField(blank=True, null=True)
    project_stakeholders = models.TextField(blank=True, null=True)
    project_start_date = models.DateField(blank=True, null=True)
    project_end_date = models.DateField(blank=True, null=True)
    project_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_project_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization.name + ' - ' + self.project_name + ' - ' + self.project_department + ' - ' + self.created_at.strftime(
            '%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Project Item'
        verbose_name_plural = 'Project Items'
        ordering = ['-created_at']
        unique_together = ('organization', 'project_name', 'project_department')
        indexes = [
            models.Index(fields=['organization', 'project_name', 'project_department']),
            models.Index(fields=['organization', 'project_name']),
            models.Index(fields=['organization']),
            models.Index(fields=['project_name']),
            models.Index(fields=['project_department']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['project_status']),
            models.Index(fields=['project_priority']),
            models.Index(fields=['project_risk_level']),
            models.Index(fields=['project_start_date']),
            models.Index(fields=['project_end_date']),
            models.Index(fields=['project_budget']),
            models.Index(fields=['created_by_user']),
        ]
