#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: team_admin.py
#  Last Modified: 2024-10-24 22:00:26
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 22:00:26
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


"""
class ProjectTeamItem(models.Model):
    project = models.ForeignKey('ProjectItem', on_delete=models.CASCADE, related_name='project_teams')
    team_members = models.ManyToManyField('auth.User', related_name='project_teams', blank=True)

    team_name = models.CharField(max_length=1000)
    team_description = models.TextField(blank=True)
    team_lead = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='led_project_teams')

    created_by_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='created_project_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.project_name + ' - ' + self.team_name + ' - ' + self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        verbose_name = 'Project Team Item'
        verbose_name_plural = 'Project Team Items'
        ordering = ['-created_at']
        unique_together = ('project', 'team_name')
        indexes = [
            models.Index(fields=['project', 'team_name']),
            models.Index(fields=['project']),
            models.Index(fields=['team_name']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
        ]

"""

from django.contrib import admin

from apps.projects.models import ProjectTeamItem
from apps.projects.utils import PROJECT_TEAM_ITEM_ADMIN_LIST, PROJECT_TEAM_ITEM_ADMIN_FILTER, \
    PROJECT_TEAM_ITEM_ADMIN_SEARCH


@admin.register(ProjectTeamItem)
class ProjectTeamItemAdmin(admin.ModelAdmin):
    list_display = PROJECT_TEAM_ITEM_ADMIN_LIST
    list_filter = PROJECT_TEAM_ITEM_ADMIN_FILTER
    search_fields = PROJECT_TEAM_ITEM_ADMIN_SEARCH
    ordering = ('project', 'team_name', 'team_lead', 'created_by_user', 'created_at')
