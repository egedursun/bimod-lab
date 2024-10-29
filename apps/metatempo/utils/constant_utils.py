#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-28 19:36:22
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-28 19:36:23
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


METATEMPO_OVERALL_LOG_INTERVALS = [
    ('daily', 'Daily'),
    ('bi-daily', 'Bi-Daily'),
    ('weekly', 'Weekly'),
    ('bi-weekly', 'Bi-Weekly'),
    ('monthly', 'Monthly'),
]


class MetaTempoOverallLogIntervalsNames:
    DAILY = 'daily'
    BI_DAILY = 'bi-daily'
    WEEKLY = 'weekly'
    BI_WEEKLY = 'bi-weekly'
    MONTHLY = 'monthly'

    @staticmethod
    def as_list():
        return [
            MetaTempoOverallLogIntervalsNames.DAILY,
            MetaTempoOverallLogIntervalsNames.BI_DAILY,
            MetaTempoOverallLogIntervalsNames.WEEKLY,
            MetaTempoOverallLogIntervalsNames.BI_WEEKLY,
            MetaTempoOverallLogIntervalsNames.MONTHLY,
        ]


METATEMPO_MEMBER_LOG_INTERVALS = [
    ('times_12_per_hour', '12 Times Per Hour'),
    ('times_6_per_hour', '6 Times Per Hour'),
    ('times_4_per_hour', '4 Times Per Hour'),
    ('times_3_per_hour', '3 Times Per Hour'),
    ('times_2_per_hour', '2 Times Per Hour'),
    ('hourly', 'Hourly'),
    ('every_2_hours', 'Every 2 Hours'),
    ('every_4_hours', 'Every 4 Hours'),
]


class MetaTempoMemberLogIntervalsNames:
    TIMES_12_PER_HOUR = 'times_12_per_hour'
    TIMES_6_PER_HOUR = 'times_6_per_hour'
    TIMES_4_PER_HOUR = 'times_4_per_hour'
    TIMES_3_PER_HOUR = 'times_3_per_hour'
    TIMES_2_PER_HOUR = 'times_2_per_hour'
    HOURLY = 'hourly'
    EVERY_2_HOURS = 'every_2_hours'
    EVERY_4_HOURS = 'every_4_hours'

    @staticmethod
    def as_list():
        return [MetaTempoMemberLogIntervalsNames.TIMES_12_PER_HOUR,
                MetaTempoMemberLogIntervalsNames.TIMES_6_PER_HOUR,
                MetaTempoMemberLogIntervalsNames.TIMES_4_PER_HOUR,
                MetaTempoMemberLogIntervalsNames.TIMES_3_PER_HOUR,
                MetaTempoMemberLogIntervalsNames.TIMES_2_PER_HOUR,
                MetaTempoMemberLogIntervalsNames.HOURLY,
                MetaTempoMemberLogIntervalsNames.EVERY_2_HOURS,
                MetaTempoMemberLogIntervalsNames.EVERY_4_HOURS]


META_TEMPO_CONNECTION_ADMIN_LIST = ['board', 'is_tracking_active', 'created_at', 'updated_at']
META_TEMPO_CONNECTION_ADMIN_FILTER = ['board', 'is_tracking_active', 'created_at', 'updated_at']
META_TEMPO_CONNECTION_ADMIN_SEARCH = ['board', 'is_tracking_active', 'created_at', 'updated_at']
META_TEMPO_MEMBER_LOG_ADMIN_LIST = ['metatempo_connection', 'user', 'timestamp', 'work_intensity']
META_TEMPO_MEMBER_LOG_ADMIN_FILTER = ['metatempo_connection', 'user', 'timestamp', 'work_intensity']
META_TEMPO_MEMBER_LOG_ADMIN_SEARCH = ['metatempo_connection', 'user', 'timestamp', 'work_intensity']
META_TEMPO_MEMBER_LOG_DAILY_ADMIN_LIST = ['metatempo_connection', 'user', 'datestamp', 'created_at']
META_TEMPO_MEMBER_LOG_DAILY_ADMIN_FILTER = ['metatempo_connection', 'user', 'datestamp', 'created_at']
META_TEMPO_MEMBER_LOG_DAILY_ADMIN_SEARCH = ['metatempo_connection', 'user', 'datestamp', 'created_at']
META_TEMPO_PROJECT_OVERALL_LOG_ADMIN_LIST = ['metatempo_connection', 'overall_work_intensity', 'created_at']
META_TEMPO_PROJECT_OVERALL_LOG_ADMIN_FILTER = ['metatempo_connection', 'overall_work_intensity', 'created_at']
META_TEMPO_PROJECT_OVERALL_LOG_ADMIN_SEARCH = ['metatempo_connection', 'overall_work_intensity', 'created_at']


META_TEMPO_CONNECTION_API_KEY_DEFAULT_LENGTH = 64
