#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: constant_utils.py
#  Last Modified: 2024-10-20 14:05:46
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-10-20 14:05:46
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#


NOTIFICATION_FA_ICON_CHOICES = [
    ('fa fa-bell', 'fa fa-bell'),
    ('fa fa-bullseye', 'fa fa-bullseye'),
    ('fa fa-comment', 'fa fa-comment'),
    ('fa fa-envelope', 'fa fa-envelope'),
    ('fa fa-exclamation-triangle', 'fa fa-exclamation-triangle'),
    ('fa fa-info-circle', 'fa fa-info-circle'),
    ('fa fa-list', 'fa fa-list'),
    ('fa fa-paper-plane', 'fa fa-paper-plane'),
    ('fa fa-question-circle', 'fa fa-question-circle'),
    ('fa fa-building', 'fa fa-building'),
]


class NotificationFAIconChoicesNames:
    BELL = 'fa fa-bell'
    BULLSEYE = 'fa fa-bullseye'
    COMMENT = 'fa fa-comment'
    ENVELOPE = 'fa fa-envelope'
    EXCLAMATION_TRIANGLE = 'fa fa-exclamation-triangle'
    INFO_CIRCLE = 'fa fa-info-circle'
    LIST = 'fa fa-list'
    PAPER_PLANE = 'fa fa-paper-plane'
    QUESTION_CIRCLE = 'fa fa-question-circle'
    BUILDING = 'fa fa-building'

    @staticmethod
    def as_list():
        return [
            NotificationFAIconChoicesNames.BELL,
            NotificationFAIconChoicesNames.BULLSEYE,
            NotificationFAIconChoicesNames.COMMENT,
            NotificationFAIconChoicesNames.ENVELOPE,
            NotificationFAIconChoicesNames.EXCLAMATION_TRIANGLE,
            NotificationFAIconChoicesNames.INFO_CIRCLE,
            NotificationFAIconChoicesNames.LIST,
            NotificationFAIconChoicesNames.PAPER_PLANE,
            NotificationFAIconChoicesNames.QUESTION_CIRCLE,
            NotificationFAIconChoicesNames.BUILDING,
        ]


NOTIFICATION_TITLE_CATEGORY_CHOICES = [
    ('bimod-team', 'Bimod Team'),
    ('internal', 'Internal Notification'),
    ('info', 'Information'),
    ('alert', 'Alert'),
    ('warning', 'Warning'),
    ('error', 'System Error'),
]


class NotificationTitleCategoryChoicesNames:
    BIMOD_TEAM = 'bimod-team'
    INTERNAL = 'internal'
    INFO = 'info'
    ALERT = 'alert'
    WARNING = 'warning'
    ERROR = 'error'

    @staticmethod
    def as_list():
        return [
            NotificationTitleCategoryChoicesNames.BIMOD_TEAM,
            NotificationTitleCategoryChoicesNames.INTERNAL,
            NotificationTitleCategoryChoicesNames.INFO,
            NotificationTitleCategoryChoicesNames.ALERT,
            NotificationTitleCategoryChoicesNames.WARNING,
            NotificationTitleCategoryChoicesNames.ERROR,
        ]

    class HumanReadable:
        BIMOD_TEAM = 'Bimod Team'
        INTERNAL = 'Internal Notification'
        INFO = 'Information'
        ALERT = 'Alert'
        WARNING = 'Warning'
        ERROR = 'System Error'

        @staticmethod
        def as_list():
            return [
                NotificationTitleCategoryChoicesNames.HumanReadable.BIMOD_TEAM,
                NotificationTitleCategoryChoicesNames.HumanReadable.INTERNAL,
                NotificationTitleCategoryChoicesNames.HumanReadable.INFO,
                NotificationTitleCategoryChoicesNames.HumanReadable.ALERT,
                NotificationTitleCategoryChoicesNames.HumanReadable.WARNING,
                NotificationTitleCategoryChoicesNames.HumanReadable.ERROR,
            ]


NOTIFICATION_ITEM_ADMIN_LIST = ('user', 'notification_fa_icon', 'notification_title_category', 'created_at')
NOTIFICATION_ITEM_ADMIN_FILTER = ('user', 'notification_fa_icon', 'notification_title_category', 'created_at')
NOTIFICATION_ITEM_ADMIN_SEARCH = ('user__username', 'notification_fa_icon', 'notification_title_category',
                                  'notification_message')
