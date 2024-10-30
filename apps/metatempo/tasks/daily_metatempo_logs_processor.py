#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: generate_daily_metatempo_logs.py
#  Last Modified: 2024-10-29 22:07:35
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 22:07:36
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#
import logging

from celery import shared_task

from apps.core.metatempo.metatempo_execution_handler import MetaTempoExecutionManager
from apps.metatempo.models import MetaTempoConnection
from apps.projects.models import ProjectItem, ProjectTeamItem


logger = logging.getLogger(__name__)


@shared_task
def generate_daily_metatempo_logs():
    # Retrieve all projects
    try:
        all_projects = ProjectItem.objects.all()
        all_team_members_by_connection = {}
        for project in all_projects:
            project: ProjectItem
            metatempo_connection = MetaTempoConnection.objects.filter(board__project=project, is_tracking_active=True).first()
            if metatempo_connection:
                for team in project.project_teams.all():
                    team: ProjectTeamItem
                    if metatempo_connection.id not in all_team_members_by_connection:
                        all_team_members_by_connection[metatempo_connection.id] = []
                    all_team_members_by_connection[metatempo_connection.id] += team.team_members.all()
    except Exception as e:
        logger.error(f"Error while aggregating the project team members: {e}")
        return False

    try:
        # Convert to unique members to avoid duplicate processing
        for connection_id, team_members in all_team_members_by_connection.items():
            all_team_members_by_connection[connection_id] = list(set(team_members))
    except Exception as e:
        logger.error(f"Error while converting the team members to unique members: {e}")
        return False

    try:
        # Process logs
        for connection_id, team_members in all_team_members_by_connection.items():
            try:
                xc = (MetaTempoExecutionManager(metatempo_connection_id=connection_id))
                _, error = xc.interpret_and_save_daily_logs_batch(users=team_members)
                if error:
                    logger.error(f"Error while processing the daily logs for connection {connection_id}: {error}")
                    continue
            except Exception as e:
                logger.error(f"Error while processing the daily logs for connection {connection_id}: {e}")
                continue

    except Exception as e:
        logger.error(f"Error while processing the daily logs: {e}")
        return False

    logger.info("Daily logs processed successfully.")
    return True
