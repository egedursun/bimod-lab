#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-05 01:39:48
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-05 14:42:45
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


TRIGGERED_JOB_INSTANCE_STATUSES = [
    ('pending', 'Pending'),
    ('building', 'Building'),
    ('initializing_assistant', 'Initializing Assistant'),
    ('generating', 'Generating'),
    ('saving_logs', 'Saving Logs'),
    ('cleaning_up', 'Cleaning Up'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]


class TriggeredJobInstanceStatusesNames:
    PENDING = 'pending'
    BUILDING = 'building'
    INITIALIZING_ASSISTANT = 'initializing_assistant'
    GENERATING = 'generating'
    SAVING_LOGS = 'saving_logs'
    CLEANING_UP = 'cleaning_up'
    COMPLETED = 'completed'
    FAILED = 'failed'


TRIGGERED_JOB_ADMIN_LIST = [
    'name',
    'trigger_assistant',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]
TRIGGERED_JOB_ADMIN_SEARCH = [
    'name',
    'trigger_assistant',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]
TRIGGERED_JOB_ADMIN_FILTER = [
    'name',
    'trigger_assistant',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]

TRIGGERED_JOB_INSTANCE_ADMIN_LIST = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]
TRIGGERED_JOB_INSTANCE_ADMIN_SEARCH = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]
TRIGGERED_JOB_INSTANCE_ADMIN_FILTER = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]


ORCHESTRATION_TRIGGERED_JOB_ADMIN_LIST = [
    'name',
    'trigger_maestro',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]
ORCHESTRATION_TRIGGERED_JOB_ADMIN_SEARCH = [
    'name',
    'trigger_maestro',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]
ORCHESTRATION_TRIGGERED_JOB_ADMIN_FILTER = [
    'name',
    'trigger_maestro',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]

LEANMOD_TRIGGERED_JOB_ADMIN_LIST = [
    'name',
    'trigger_leanmod',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]
LEANMOD_TRIGGERED_JOB_ADMIN_SEARCH = [
    'name',
    'trigger_leanmod',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]
LEANMOD_TRIGGERED_JOB_ADMIN_FILTER = [
    'name',
    'trigger_leanmod',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user'
]

ORCHESTRATION_TRIGGERED_JOB_INSTANCE_ADMIN_LIST = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]
ORCHESTRATION_TRIGGERED_JOB_INSTANCE_ADMIN_SEARCH = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]
ORCHESTRATION_TRIGGERED_JOB_INSTANCE_ADMIN_FILTER = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]



LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_LIST = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]
LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_SEARCH = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]
LEANMOD_TRIGGERED_JOB_INSTANCE_ADMIN_FILTER = [
    'triggered_job',
    'status',
    'started_at',
    'ended_at'
]
