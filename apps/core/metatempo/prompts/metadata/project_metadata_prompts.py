#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: project_metadata_prompts.py
#  Last Modified: 2024-10-29 19:52:43
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-29 19:52:44
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

from apps.metakanban.models import (
    MetaKanbanBoard,
    MetaKanbanTaskLabel,
    MetaKanbanTask,
    MetaKanbanChangeLog,
    MetaKanbanStatusColumn
)

from apps.projects.models import (
    ProjectItem,
    ProjectTeamItem
)

from apps.core.metakanban.utils import (
    METAKANBAN_DEFAULT_LAST_N_ACTION_LOGS_LOOKBACK
)


def get_board_metadata_prompt(board: MetaKanbanBoard):
    return f"""
        -----

        ### **BOARD METADATA:**

        -----

        [Board ID: {board.id}]
        [Board Title: {board.title}]
        [Board Description: {board.description}]
        ***

        -----

        - **NOTE:** The board metadata listed here is the board chosen to be managed with you as a Project Tempo &
        Performance manager assistant, and to provide you more context while you are interpreting the team performance
        as well as the efficiency, and keep you aware of the current tasks in the project's kanban board. This is also
        to help  you understand the context of the queries delivered to your by the user in a better way. For example,
        if the user tells about a certain problem, you can use your knowledge about the tasks, project and the team.
        Further information about this is shared in your system prompt.
    """


def get_board_labels_metadata_prompt(board: MetaKanbanBoard):
    board_labels = board.metakanbantasklabel_set.all()
    board_labels_prompt = f"""
        -----

        ### **BOARD LABELS:**

        -----

        '''
    """

    for board_label in board_labels:
        board_label: MetaKanbanTaskLabel
        board_labels_prompt += f"""
            [Label ID: {board_label.id}]
            [Label Name: {board_label.label_name}]
            [Label Color in HEX: {board_label.label_color}]
            ***
            '''
        """

    board_labels_prompt += "'''\n"

    return f"""
        {board_labels_prompt}

        - **NOTE:** The labels listed here are the labels that are already existing in the board you are managing the
        team performance & efficiency of. You can use this information to understand the current state of the team and
        the tempo of the team, and the labels within the board can help you have more context about the project.
        Further information about this is shared in your system prompt.

        -----

    """


def get_board_existing_tasks_metadata_prompt(board: MetaKanbanBoard):
    board_columns = board.metakanbanstatuscolumn_set.all()
    board_columns_prompt = f"""
        -----

        ### **BOARD EXISTING COLUMNS AND THE EXISTING TASKS IN THE COLUMNS:**

        -----
    """

    for board_column in board_columns:
        board_column: MetaKanbanStatusColumn
        board_columns_prompt += f"""
        '''
            [Status Column ID: {board_column.id}]
            [Status Column Name: {board_column.column_name}]
            [Status Column Position ID: {board_column.position_id}]
            [Status Tasks in this Column]
            ***
        '''
        """

        column_tasks = MetaKanbanTask.objects.filter(status_column=board_column).all()
        for column_task in column_tasks:
            column_task: MetaKanbanTask
            board_columns_prompt += f"""
                [Task ID: {column_task.id}]
                [Task Title: {column_task.title}]
                [Task Description: {column_task.description}]
                [Task Priority: {column_task.priority}]
                [Task Due Date: {str(column_task.due_date)}]
                [Task URL: {column_task.task_url}]

                [Task Assignees]
                    '''
            """

            task_assignees = column_task.assignees.all()
            for task_assignee in task_assignees:
                task_assignee: User
                board_columns_prompt += f"""
                    [Assignee User ID: {task_assignee.id}]
                    [Assignee User: {task_assignee.profile.first_name} {task_assignee.profile.last_name}]
                    ***
                    '''
                """
            board_columns_prompt += "'''\n"
        board_columns_prompt += "'''\n"
    board_columns_prompt += "'''\n"

    return f"""
        {board_columns_prompt}

        - **NOTE:** The tasks listed here are the tasks that are already existing in the columns of the Kanban board
        that you are tracking the team performance and efficiency of. You can use this information to understand the
        current state of the project, team and the board and the tasks within the board. This information can also be
        used to understand the context of the queries delivered to you by the user in a better way. For example, if the
        user asks you about a certain status of an individual or a project, you can use your knowledge about the project
        status, tasks, labels, assignees, etc to provide a higher quality answer. Further information about this is
        shared in your system prompt.

        -----

    """


def get_metakanban_last_n_action_logs_prompt(board: MetaKanbanBoard):
    logs = board.meta_kanban_change_logs.all().order_by('-timestamp')
    if logs.count() > METAKANBAN_DEFAULT_LAST_N_ACTION_LOGS_LOOKBACK:
        logs = logs[:METAKANBAN_DEFAULT_LAST_N_ACTION_LOGS_LOOKBACK]

    logs_prompt = f"""
        -----

        ### **LAST {METAKANBAN_DEFAULT_LAST_N_ACTION_LOGS_LOOKBACK} ACTION LOGS:**

        -----

        '''
    """

    for log in logs:
        log: MetaKanbanChangeLog
        logs_prompt += f"""
            [Log ID: {log.id}]
            [Action Type: {log.action_type}]
            [Action Details: {log.action_details}]
            [Timestamp of Action: {log.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]
            ***
            '''
        """

    logs_prompt += "'''\n"

    return f"""
        {logs_prompt}

        - **NOTE:** The logs listed here are the last {METAKANBAN_DEFAULT_LAST_N_ACTION_LOGS_LOOKBACK} action logs
        that are recorded in the Kanban board you are managing the team tempo, efficiency and performance of. You can
        use this information to understand the recent actions taken in the board and therefore the project. This can
        be used to understand the context of the queries delivered to you by the user in  a better way. For example, if
        the user tells about the overall performance of the team (or it might be an individual, or some other question),
        you can use your knowledge to provide the users answers with higher quality. Further information about this is
        shared in your system prompt.

        -----
    """


def get_metakanban_project_metadata_prompt(board: MetaKanbanBoard):
    project_item: ProjectItem = board.project
    project_item_prompt = ""
    project_item_prompt += f"""

        -----

        ### **PROJECT METADATA:**

        -----

        [Project ID: {project_item.id}]
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
        project_item_prompt += f"""
            [Team ID: {project_team.id}]
            [Team Name: {project_team.team_name}]
            [Team Description: {project_team.team_description}]
            [Team Lead: {project_team.team_lead.profile.first_name} {project_team.team_lead.profile.last_name}]
            [Team Members]
            '''
            """

        team_members = project_team.team_members.all()
        for team_member in team_members:
            team_member: User
            project_item_prompt += f"""
                '''
                [Team Member User ID: {team_member.id}]
                [Team Member: {team_member.profile.first_name} {team_member.profile.last_name}]
                '''
                ***
                """
            project_item_prompt += "'''\n"
        project_item_prompt += "'''\n"
        pass
    pass

    return f"""
        ### **RELATED PROJECT OF ASSISTANT:**

        **NOTE**: The project listed here is the project chosen to be managed with you as a Team Tempo, performance and
        efficiency manager and tracker assistant, and to provide you more context while you are tracking, analyzing and
        interpreting the team status, efficiency and performance within the context of the project. This is also to
        help you understand the context of the queries delivered to your by the user in a better way. For example, if
        the user tells about a certain individual and his risky behavior or idle status, you can use your knowledge to
        comparatively understand and analyze the project goals, tasks and the behavior of the user according to tracking
        logs you have received for the user.

        '''
        {project_item_prompt}
        '''

        -----
    """
