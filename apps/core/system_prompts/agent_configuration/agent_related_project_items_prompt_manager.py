#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: agent_related_project_items_prompt_manager.py
#  Last Modified: 2024-10-24 23:41:52
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-24 23:41:53
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

from django.contrib.auth.models import User

from apps.assistants.models import (
    Assistant
)

from apps.projects.models import (
    ProjectItem,
    ProjectTeamItem
)


def build_agent_related_project_items_prompt(agent: Assistant) -> str:

    project_items_prompt = ""
    for project_item in agent.project_items.all():
        project_item: ProjectItem
        project_items_prompt += f"""
            ---
            [Project Name: {project_item.project_name}]
            [Project Department: {project_item.project_department}]
            [Project Description: {project_item.project_description}]
            [Project Status: {project_item.project_status}]
            [Project Priority: {project_item.project_priority}]
            [Project Risk Level: {project_item.project_risk_level}]
            [Project Constraints: {project_item.project_constraints}]
            [Project Stakeholders: {project_item.project_stakeholders}]
            [Project Budget: {str(project_item.project_budget)}]
            [Project Start Date: {str(project_item.project_start_date)}]
            [Project End Date: {str(project_item.project_end_date)}]
            [Project Teams]
                '''
        """
        project_teams = project_item.project_teams.all()
        for project_team in project_teams:
            project_team: ProjectTeamItem
            project_items_prompt += f"""
                [Team Name: {project_team.team_name}]
                [Team Description: {project_team.team_description}]
                [Team Lead: {project_team.team_lead.profile.first_name} {project_team.team_lead.profile.last_name}]
                [Team Members]
                    '''
            """

            team_members = project_team.team_members.all()
            for team_member in team_members:
                team_member: User
                project_items_prompt += f"""
                    [Team Member: {team_member.profile.first_name} {team_member.profile.last_name}]
                """
            project_items_prompt += "'''\n"
        project_items_prompt += "'''\n"
        pass
    pass

    return f"""
        ### **RELATED PROJECTS OF ASSISTANT:**

        **NOTE**: The projects listed here are the projects chosen to be associated with you as an assistant, and to
        provide you more context while you are assisting users, and to help you understand the context of the
        conversation better. For example, if the user tells about a certain problem without specifying the project,
        you can use the context of the projects listed here to understand the problem better and provide more accurate
        assistance.

        '''
        {project_items_prompt}
        '''

        -----
    """
