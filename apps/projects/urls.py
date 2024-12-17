#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: urls.py
#  Last Modified: 2024-10-24 21:59:11
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 21:59:11
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.urls import path

from apps.projects.views import (
    ProjectsView_ProjectCreate,
    ProjectsView_TeamCreate,
    ProjectsView_TeamDelete,
    ProjectsView_TeamList,
    ProjectsView_ProjectList,
    ProjectsView_ProjectDelete,
    ProjectsView_ProjectUpdate,
    ProjectsView_TeamUpdate
)

app_name = 'projects'

urlpatterns = [
    path(
        "project/create/",
        ProjectsView_ProjectCreate.as_view(
            template_name="projects/project/create_project.html"
        ),
        name="project_create"
    ),

    path(
        "project/list/",
        ProjectsView_ProjectList.as_view(
            template_name="projects/project/list_projects.html"
        ),
        name="project_list"
    ),

    path(
        "project/update/<int:pk>/",
        ProjectsView_ProjectUpdate.as_view(
            template_name="projects/project/update_project.html"
        ),
        name="project_update"
    ),

    path(
        "project/delete/<int:pk>/",
        ProjectsView_ProjectDelete.as_view(
            template_name="projects/project/confirm_delete_project.html"
        ),
        name="project_delete"
    ),

    #####

    path(
        "team/create/",
        ProjectsView_TeamCreate.as_view(
            template_name="projects/team/create_team.html"
        ),
        name="team_create"
    ),

    path(
        "team/list/",
        ProjectsView_TeamList.as_view(
            template_name="projects/team/list_teams.html"
        ),
        name="team_list"
    ),

    path(
        "team/update/<int:pk>/",
        ProjectsView_TeamUpdate.as_view(
            template_name="projects/team/update_team.html"
        ),
        name="team_update"
    ),

    path(
        "team/delete/<int:pk>/",
        ProjectsView_TeamDelete.as_view(
            template_name="projects/team/confirm_delete_team.html"
        ),
        name="team_delete"
    ),
]
