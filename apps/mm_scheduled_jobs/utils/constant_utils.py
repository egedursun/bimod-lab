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

class TriggerTypeChoicesNames:
    INTERVAL = 'interval'
    CHRONOLOGICAL = 'chronological'


SCHEDULED_JOB_INSTANCE_STATUSES = [
    ('pending', 'Pending'),
    ('building', 'Building'),
    ('initializing_assistant', 'Initializing Assistant'),
    ('generating', 'Generating'),
    ('saving_logs', 'Saving Logs'),
    ('cleaning_up', 'Cleaning Up'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]


class ScheduledJobInstanceStatusesNames:
    PENDING = 'pending'
    BUILDING = 'building'
    INITIALIZING_ASSISTANT = 'initializing_assistant'
    GENERATING = 'generating'
    SAVING_LOGS = 'saving_logs'
    CLEANING_UP = 'cleaning_up'
    COMPLETED = 'completed'
    FAILED = 'failed'


SCHEDULED_JOB_ADMIN_LIST = [
    'name',
    'assistant',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]
SCHEDULED_JOB_ADMIN_SEARCH = [
    'name',
    'assistant',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]
SCHEDULED_JOB_ADMIN_FILTER = [
    'name',
    'assistant',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]

SCHEDULED_JOB_INSTANCE_ADMIN_LIST = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]
SCHEDULED_JOB_INSTANCE_ADMIN_SEARCH = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]
SCHEDULED_JOB_INSTANCE_ADMIN_FILTER = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]

ORCHESTRATION_SCHEDULED_JOB_ADMIN_LIST = [
    'name',
    'maestro',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]
ORCHESTRATION_SCHEDULED_JOB_ADMIN_SEARCH = [
    'name',
    'maestro',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]
ORCHESTRATION_SCHEDULED_JOB_ADMIN_FILTER = [
    'name',
    'maestro',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]

ORCHESTRATION_SCHEDULED_JOB_INSTANCE_ADMIN_LIST = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]
ORCHESTRATION_SCHEDULED_JOB_INSTANCE_ADMIN_SEARCH = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]
ORCHESTRATION_SCHEDULED_JOB_INSTANCE_ADMIN_FILTER = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]

LEANMOD_SCHEDULED_JOB_ADMIN_LIST = [
    'name',
    'leanmod',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]

LEANMOD_SCHEDULED_JOB_ADMIN_SEARCH = [
    'name',
    'leanmod',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]

LEANMOD_SCHEDULED_JOB_ADMIN_FILTER = [
    'name',
    'leanmod',
    'current_run_count',
    'maximum_runs',
    'created_at',
    'updated_at',
    'created_by_user',
]

LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_LIST = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]

LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_SEARCH = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]

LEANMOD_SCHEDULED_JOB_INSTANCE_ADMIN_FILTER = [
    'scheduled_job',
    'status',
    'started_at',
    'ended_at'
]
